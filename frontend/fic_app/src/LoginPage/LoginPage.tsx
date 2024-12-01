import React, { useState } from "react";
import { fetchLogin } from "../Requests/getInfo";
import classes from "./LoginPage.module.css";
import Button from "../components/Button/Button";
import { usePage } from "../Contexts/PageContext/PageContext";
const LoginPage: React.FC = () => {
    const [login, setLogin] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        fetchLogin(login, password);
    };
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { currentPage, setCurrentPage } = usePage();
    return (
        <div className="container">
            <form className={classes.form} onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={login}
                    onChange={(e) => setLogin(e.target.value)}
                    required
                    placeholder="Имя"
                />
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    placeholder="Пароль"
                />
                <Button text="Войти" type="submit" />
                <span>
                    Нет аккаунта?{" "}
                    <button
                        className={classes.registerButton}
                        onClick={() => {
                            setCurrentPage("REGISTER");
                        }}
                    >
                        Зарегистрироваться
                    </button>
                </span>
            </form>
        </div>
    );
};

export default LoginPage;
