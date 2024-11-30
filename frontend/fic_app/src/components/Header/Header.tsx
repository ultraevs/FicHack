import logo from "../../assets/images/logo.svg";
import { usePage } from "../../Contexts/PageContext/PageContext";
import NavBar from "../NavBar/NavBar";
import classes from "./Header.module.css";

const Header = () => {
    const setCurrentPage = usePage().setCurrentPage;
    return (
        <header className={classes.header}>
            <div className="container">
                <div className={classes.headerWrapper}>
                    <button
                        type="button"
                        onClick={() => setCurrentPage("MAIN")}
                    >
                        <img src={logo} alt="shmyaks" />
                    </button>
                    <NavBar />
                </div>
            </div>
        </header>
    );
};

export default Header;
