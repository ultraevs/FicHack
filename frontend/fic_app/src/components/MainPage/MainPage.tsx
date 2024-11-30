import classes from "./MainPage.module.css";
import promoImage from "../../assets/images/promo-image.png";
import Button from "../Button/Button";
const MainPage = () => {
    return (
        <section className={classes.mainPage}>
            <div className="container">
                <div className={classes.flexbox}>
                    <div className={classes.content}>
                        <div className={classes.textbox}>
                            <h1 className={classes.title}>
                                ФИЦ 2024: <span>Хакатон</span>
                            </h1>
                            <h2 className={classes.subtitle}>
                                Разработка модуля классификации опор ЛЭП
                            </h2>
                            <span className={classes.team}>
                                Команда shmyaks MISIS: Брежнев Артём, Лобода
                                Иван, Ломаев Илья, Таланцев Глеб, Евсеев Михаил
                            </span>
                        </div>
                        <Button text="К интерфейсу" />
                    </div>
                    <img
                        className={classes.promoImage}
                        src={promoImage}
                        alt="Изображение интерфейса"
                    />
                </div>
            </div>
        </section>
    );
};

export default MainPage;
