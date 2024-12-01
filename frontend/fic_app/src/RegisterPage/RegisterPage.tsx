import React, { useState } from "react";
import { fetchRegister } from "../Requests/getInfo";
import classes from "./RegisterPage.module.css";
import Button from "../components/Button/Button";
import { usePage } from "../Contexts/PageContext/PageContext";

const RegisterPage: React.FC = () => {
    const [login, setLogin] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        fetchRegister(login, password);
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
                <Button text="Зарегистрироваться" type="submit" />
                <span>
                    Есть аккаунт?
                    <button
                        className={classes.enterButton}
                        onClick={() => {
                            setCurrentPage("LOGIN");
                        }}
                    >
                        Войти
                    </button>
                </span>
            </form>
        </div>
    );
};

export default RegisterPage;
