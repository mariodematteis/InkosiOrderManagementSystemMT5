import random
import string

import numpy as np
import pandas as pd
import requests
import streamlit as st
from fastapi import status

from inkosi.database.postgresql.database import PostgreSQLCrud
from inkosi.database.postgresql.schemas import FundInformation
from inkosi.log.log import Logger
from inkosi.utils.utils import AdministratorPolicies, InvestorPolicies

logger = Logger(module_name="app", package_name="web")

st.set_page_config(page_title="Inkosi Web App - Login")


def get_authentication() -> bool:
    session = st.session_state
    token = session.get("token", "")
    if not token:
        logger.critical("The token has not been found")
        return False

    postgres = PostgreSQLCrud()
    result = postgres.valid_authentication(
        token,
    )
    if not result:
        set_token("")

    return result


def set_token(token: str) -> None:
    session = st.session_state
    session["token"] = token


def generate_id(length: int) -> str:
    return "".join(
        [
            random.choice(
                list(
                    set(string.ascii_uppercase)
                    .union(string.ascii_lowercase)
                    .union(set(string.digits))
                )
            )
            for _ in range(length)
        ]
    )


state = get_authentication()

if state:
    # st.set_page_config(page_title="Inkosi")

    if "generate_id" not in st.session_state:
        st.session_state["generate_id"] = generate_id(12)

    request_list_funds = requests.get(
        url="http://localhost:44444/api/v1/list_funds", timeout=8000
    )

    if request_list_funds.status_code != status.HTTP_200_OK:
        st.error(f"Server Response - {request_list_funds.json().get('detail', '')}")

    raw_funds_list: dict = request_list_funds.json()

    funds_list: list[str] = [
        str(fund.get("fund_name", "NA")) for fund in raw_funds_list
    ]
    fund_selected = st.sidebar.selectbox(
        "Fund Name",
        options=funds_list,
    )

    request_fund_information = requests.get(
        url=f"http://localhost:44444/api/v1/fund?fund_name={fund_selected}",
        timeout=8000,
    )

    if request_fund_information.status_code != status.HTTP_200_OK:
        st.error(
            f"Server Response - {request_fund_information.json().get('detail', '')}"
        )

    fund_information: FundInformation = FundInformation(
        **request_fund_information.json().get("result", {})
    )

    administrators: list = (
        ", ".join(
            "<strong>" + administrator + "</strong>"
            for administrator in fund_information.administrator
        )
        if fund_information.administrator
        else "<strong>-</strong>"
    )
    investors: list[str] = (
        ", ".join(
            "<strong>" + investor + "</strong>"
            for investor in fund_information.investors
        )
        if fund_information.investors
        else "<strong>-</strong>"
    )

    raw_commission_type: str = fund_information.commission_type

    commission_type: str = (
        "<strong>"
        f"{'-' if raw_commission_type is None else raw_commission_type}</strong>"
    )

    raw_commission_value: str = fund_information.commission_value

    commission_value: str = (
        "<strong>"
        f"{'-' if raw_commission_value is None else raw_commission_value}</strong>"
    )

    st.sidebar.markdown(
        body=f"""
        <p>Investment Firm <strong>{fund_information.investment_firm}</strong></p>
        <p>Fund Name <strong>{fund_information.fund_name}</strong></p>
        <p>Administrator {administrators}</p>
        <p>Investors {investors}</p>
        <p>Commission Type {commission_type}</p>
        <p>Commission Value {commission_value}</p>
        """,
        unsafe_allow_html=True,
    )

    investor_expander = st.sidebar.expander(
        label="Investor",
    )
    investor_first_name = investor_expander.text_input(
        label="Investor - First Name",
        placeholder="First Name",
        label_visibility="hidden",
    )
    investor_second_name = investor_expander.text_input(
        label="Investor - Second Name",
        placeholder="Second Name",
        label_visibility="hidden",
    )
    investor_email_address = investor_expander.text_input(
        label="Investor - E-mail Address",
        placeholder="E-mail Address",
        label_visibility="hidden",
    )
    investor_policies = investor_expander.multiselect(
        label="Investor - Policies",
        placeholder="Select policies (these are additional)",
        options=InvestorPolicies.list(),
        label_visibility="hidden",
    )
    if investor_expander.button(
        "Add Investor",
        use_container_width=True,
    ):
        if (
            not investor_email_address
            or not investor_first_name
            or not investor_second_name
        ):
            st.error(
                "Unable to create a new investor, not enough information specified",
                icon="🚨",
            )

        if fund_information.fund_raising:
            st.error(
                "The Fund Raising Phase has been closed",
                icon="🚨",
            )

        password = "".join(
            [
                random.choice(
                    list(
                        set(string.ascii_letters)
                        .union(string.ascii_lowercase)
                        .union(string.ascii_uppercase)
                    )
                )
                for _ in range(12)
            ]
        )

        request = requests.post(
            url="http://localhost:44444/api/v1/create_administrator",
            json={
                "first_name": investor_first_name,
                "second_name": investor_second_name,
                "email_address": investor_email_address,
                "policies": investor_policies,
                "password": password,
            },
            headers={
                "Content-Type": "application/json",
            },
            timeout=8000,
        )

        if request.status_code == status.HTTP_200_OK:
            st.info(
                "A new investor account has been created. These are the"
                f" credentials: E-mail Address{investor_email_address} - Password:"
                f" {password}",
                icon="ℹ️",
            )

    administrator_expander = st.sidebar.expander(label="Administrator")
    administrator_first_name = administrator_expander.text_input(
        label="Administrator First Name",
        placeholder="First Name",
        label_visibility="hidden",
    )
    administrator_second_name = administrator_expander.text_input(
        label="Administrator Second Name",
        placeholder="Second Name",
        label_visibility="hidden",
    )
    administrator_email_address = administrator_expander.text_input(
        label="Adminitrator E-mail Address",
        placeholder="E-mail Address",
        label_visibility="hidden",
    )
    administrator_policies = administrator_expander.multiselect(
        label="Administrator Policies",
        placeholder="Select policies (these are additional)",
        options=AdministratorPolicies.list(),
        label_visibility="hidden",
    )
    if administrator_expander.button(
        "Add Admininistrator",
        use_container_width=True,
    ):
        eligible = False
        if (
            not administrator_email_address
            or not administrator_first_name
            or not administrator_second_name
        ):
            st.error(
                "Unable to create a new administrator, not enough information"
                " specified",
                icon="🚨",
            )
        else:
            eligible = True

        if not administrator_policies:
            st.warning(
                "No policies have been specified",
                icon="⚠️",
            )

        if eligible:
            password = generate_id(10)

            request = requests.post(
                url="http://localhost:44444/api/v1/create_administrator",
                json={
                    "first_name": administrator_first_name,
                    "second_name": administrator_second_name,
                    "email_address": administrator_email_address,
                    "policies": administrator_policies,
                    "password": password,
                },
                headers={
                    "Content-Type": "application/json",
                },
                timeout=8000,
            )

            if request.status_code == status.HTTP_200_OK:
                st.info(
                    "A new administrator account has been created. These are the"
                    f" credentials: E-mail Address{administrator_email_address} -"
                    f" Password: {password}",
                    icon="ℹ️",
                )

    ats_expander = st.sidebar.expander(label="Algorithmic Trading Strategy")
    ats_expander.markdown(
        "<p>Generated"
        f" ID</p><p><strong>{st.session_state.get('generate_id', 'NA')}</strong></p>",
        unsafe_allow_html=True,
    )

    if ats_expander.button("Update ID", use_container_width=True):
        st.session_state["generate_id"] = generate_id(16)

    ats_expander.text_input(
        label="Strategy Name",
        placeholder="Strategy Name",
        label_visibility="hidden",
    )

    if ats_expander.button(
        "Add ATS",
        use_container_width=True,
    ):
        ...

    fund_raising_subtitle = '<h3 style="text-align: center;">(Fund Raising Phase)</h3>'

    st.markdown(
        f"""
        <h1 style='text-align: center;'>
        {'Welcome!' if not fund_selected else fund_selected}</h1>
        {fund_raising_subtitle if fund_information.fund_raising else ''}
        """,
        unsafe_allow_html=True,
    )

    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=["col1", "col2", "col3"],
    )

    st.line_chart(
        chart_data,
        x="col1",
        y=["col2", "col3"],
        color=["#FF0000", "#0000FF"],  # Optional
    )

    st.markdown(
        """
        <h2><strong>Fund Returns Information</strong></h2>
        <p>Here </p>
        <p>Capital Gain - </p>
        """,
        unsafe_allow_html=True,
    )


else:
    st.markdown(
        "<h1 style='text-align: center;'>Inkosi Login</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        The current page let both investor and admistrator to *view* and *manage* 
        __funds__.
        <br>
        <br>
        It is important to highlight the different authentication methods available for 
        _Administrator_ and _Investors_.
        <br>
        <br>
        In particular, for the first, the __only authentication method__ *allowed* 
        accept the respective Administrator. Whereas, the __Investor authentication 
        method__ refers to the respective *E-Mail Address*.
        """,
        unsafe_allow_html=True,
    )

    username = st.text_input(
        label="E-Mail Address",
        placeholder="E-Mail Address / Administrator ID",
        label_visibility="collapsed",
    )
    password = st.text_input(
        label="Password",
        placeholder="Password",
        type="password",
        label_visibility="collapsed",
    )

    if st.button("Login", use_container_width=True):
        r = requests.get(
            url="http://localhost:44444/api/v1/login",
            json={
                "email_address": username,
                "password": password,
            },
            headers={
                "Content-Type": "application/json",
            },
            timeout=8000,
        )

        if r.status_code == status.HTTP_200_OK:
            st.session_state.token = r.json().get("token", "")
            set_token(st.session_state.token)
            st.rerun()
        else:
            st.error(f"Server Response - {r.json().get('detail', '')}")
