import { FC } from "react";
import classes from "./PhotoInformationCard.module.css";
import lockIcon from "../../assets/images/lock-keyhole.svg";

interface PhotoInformationCardProps {
    classOfSupport: string;
    ID: number;
    conf: number;
    time_taken: number;
}

type Props = PhotoInformationCardProps | null;

const PhotoInformationCard: FC<{ props: Props }> = ({ props }) => {
    if (props) {
        return (
            <div className={classes.card}>
                <span>{`Класс опоры: ${props.classOfSupport}`}</span>
                <span>{`ID: ${props.ID}`}</span>
                <span>{`Ср. уверенность: ${props.conf}`}</span>
                <span>{`Time Taken: ${props.time_taken}`}</span>
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
