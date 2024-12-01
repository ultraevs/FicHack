import Button from "../Button/Button";
import classes from "./NavBar.module.css";
import { usePage, Page } from "../../Contexts/PageContext/PageContext";

const data: Page[] = ["MAIN", "INTERFACE", "PHOTOS", "HISTORY", "LOGIN"];

enum Menu {
    "MAIN" = "Главная",
    "INTERFACE" = "Интерфейс",
    "PHOTOS" = "Множество фото",
    "HISTORY" = "История",
    "LOGIN" = "Войти",
}

const NavBar = () => {
    const { currentPage, setCurrentPage } = usePage();
    return (
        <nav className={classes.nav}>
            {data.map((item, i) => (
                <Button
                    key={i}
                    text={Menu[item as keyof typeof Menu]}
                    isActive={currentPage == item ? true : false}
                    theme="ghost"
                    onClick={() => setCurrentPage(item)}
                />
            ))}
        </nav>
    );
};

export default NavBar;
