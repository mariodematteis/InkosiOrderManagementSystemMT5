let database_name_production = process.env.DB_NAME_PRODUCTION;
let username_production = process.env.DB_USERNAME_PRODUCTION;
let password_production = process.env.DB_PASSWORD_PRODUCTION;
let user_role_production = process.env.DB_ROLE_PRODUCTION;

db.createUser(
    {
        user: username_production,
        pwd: password_production,
        roles: [
            {
                role: user_role_production,
                db: database_name_production
            }
        ]
    }
)
