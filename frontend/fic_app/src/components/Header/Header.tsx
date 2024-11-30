import logo from "../../assets/images/logo.svg";
import NavBar from "../NavBar/NavBar";
import classes from "./Header.module.css";

const Header = () => {
    return (
        <header className={classes.header}>
            <div className="container">
                <div className={classes.headerWrapper}>
                    <img src={logo} alt="shmyaks" />
                    <NavBar />
                </div>
            </div>
        </header>
    );
};

export default Header;
