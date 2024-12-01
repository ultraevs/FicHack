import { FC } from "react";
import "./StateLabelLoadingStyles.css";
import classes from "./StateLabel.module.css";

export type State = "LOADING" | "SUCCESS" | "ERROR";

interface StateLabelProps {
    state: State;
}

const StateLabel: FC<StateLabelProps> = ({ state }) => {
    switch (state) {
        case "LOADING":
            return (
                <div className="spinnerWrapper">
                    <div id="loading-bar-spinner" className="spinner">
                        <div className="spinner-icon"></div>
                    </div>
                </div>
            );
        case "SUCCESS":
            return (
                <span className={`${classes.label} ${classes.successLabel}`}>
                    Успешно
                </span>
            );
        case "ERROR":
            return (
                <span className={`${classes.label} ${classes.errorLabel}`}>
                    Ошибка
                </span>
            );
    }
};

export default StateLabel;
