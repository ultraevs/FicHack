import { FC } from "react";
import classes from "./PhotoInformationCard.module.css";
import lockIcon from "../../assets/images/lock-keyhole.svg";

export interface PhotoInformationCardProps {
    classOfSupport: string;
    ID: number;
    conf: number;
    time_taken: number;
}

type Props = PhotoInformationCardProps | null;

const PhotoInformationCard: FC<{ props: Props }> = ({ props }) => {
    if (props) {
        return (
            <div className={classes.cardWrapper}>
                <div className={`${classes.cardInfo} ${classes.cardItem}`}>
                    <div className={classes.cardInfoWrapper}>
                        <h3>Класс опоры</h3>
                        <span>{props.classOfSupport}</span>
                    </div>
                    <div className={classes.cardInfoWrapper}>
                        <h3>ID</h3>
                        <span>{props.ID}</span>
                    </div>
                    <div className={classes.cardInfoWrapper}>
                        <h3>Ср. уверенность</h3>
                        <span>{props.conf}</span>
                    </div>
                    <div className={classes.cardInfoWrapper}>
                        <h3>Time taken</h3>
                        <span>{props.time_taken}ms</span>
                    </div>
                </div>
                <div className={`${classes.cardModes} ${classes.cardItem}`}>
                    <h3>Режимы разметки</h3>
                    <span>
                        Слайдер, разметка прямоугольниками, разметка с
                        подписями,стоковое фото
                    </span>
                </div>
            </div>
        );
    }
    return (
        <div className={classes.emptyCard}>
            <img src={lockIcon} className={classes.image} alt="Заблокировано" />
            <span className={classes.lockedText}>
                Добавьте фото, чтобы получить больше информации
            </span>
        </div>
    );
};

export default PhotoInformationCard;
