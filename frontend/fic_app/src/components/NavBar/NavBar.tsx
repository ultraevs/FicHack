import Button from "../Button/Button";
import classes from "./NavBar.module.css";

const data: string[] = ["MAIN", "INTERFACE", "PHOTOS", "HISTORY", "LOGIN"];

enum Menu {
    "MAIN" = "Главная",
    "INTERFACE" = "Интерфейс",
    "PHOTOS" = "Множество фото",
    "HISTORY" = "История",
    "LOGIN" = "Войти",
}

const NavBar = () => {
    const currentPage = "MAIN";
    return (
        <nav className={classes.nav}>
            {data.map((item, i) => (
                <Button
                    key={i}
                    text={Menu[item as keyof typeof Menu]}
                    isActive={currentPage == item ? true : false}
                    theme="ghost"
                />
            ))}
        </nav>
    );
};

export default NavBar;
