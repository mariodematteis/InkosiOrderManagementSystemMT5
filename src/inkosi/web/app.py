import requests
import streamlit as st
from fastapi import status

from inkosi.database.postgresql.database import PostgreSQLCrud
from inkosi.database.postgresql.schemas import FundInformation
from inkosi.log.log import Logger

logger = Logger(module_name="app", package_name="web")


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


state = get_authentication()

if state:
    # st.set_page_config(page_title="Inkosi")

    fund_information: FundInformation = requests.get(
        url="http://localhost:44444/api/v1/fund",
        timeout=8000,
    )

    fund_selected = st.sidebar.selectbox("Fund Name", options=["pROVA", "dadw"])
    st.sidebar.text(
        body="""
        Investment Firm: {fund_information.investment_firm}
        Fund Name: {fund_information.fund_name}
        Administrator: {', '.join(administrator for administrator in fund_information.administrators)}
        Investors: {', '.join(investor for investor in fund_information.investors)}
        Commission Type: {fund_information.commission_type}
        Commission Value: {fund_information.commission_value}
        """
    )

    investor_expander = st.sidebar.expander(label="Investor")
    investor_expander.text_input(
        label="Investor",
        placeholder="New Investor",
        label_visibility="hidden",
    )
    if investor_expander.button("Add Investor"):
        ...

    administrator_expander = st.sidebar.expander(label="Administrator")
    administrator_expander.text_input(
        label="E-mail Address",
        placeholder="E-mail Address",
        label_visibility="hidden",
    )
    if administrator_expander.button("Add Admininistrator"):
        ...

    ats_expander = st.sidebar.expander(label="Algorithmic Trading Strategy")
    ats_expander.text_input(
        label="Strategy Name",
        placeholder="Strategy Name",
        label_visibility="hidden",
    )
    if ats_expander.button("Add ATS"):
        ...

    st.markdown(
        "<h1 style='text-align:"
        f" center;'>{'Welcome!' if not fund_selected else fund_selected}</h1>",
        unsafe_allow_html=True,
    )


else:
    # st.set_page_config(page_title="Inkosi Web App - Login")

    st.markdown(
        "<h1 style='text-align: center;'>Inkosi Login</h1>", unsafe_allow_html=True
    )
    st.markdown(
        """
    The current page let both investor and admistrator to manage funds, through
    the policies it is possible to monitor features
    """
    )

    username = st.text_input(
        label="E-Mail Address",
        placeholder="E-Mail Address",
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
