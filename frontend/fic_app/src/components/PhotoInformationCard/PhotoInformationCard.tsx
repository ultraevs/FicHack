import { FC } from "react";
import classes from "./PhotoInformationCard.module.css";
import lockIcon from "../../assets/images/lock-keyhole.svg";
import IconButton from "../IconButton/IconButton";
import { useTab } from "../../Contexts/TabsContext/TabsContext";

export interface PhotoInformationCardProps {
    objects: string;
    ID: number;
    "avg-conf": number;
    "time-taken": number;
}

type Props = PhotoInformationCardProps | null;

const PhotoInformationCard: FC<{ props: Props }> = ({ props }) => {
    const { currentTab, setCurrentTab } = useTab();
    if (props) {
        return (
            <div className={classes.cardWrapper}>
                <div className={`${classes.cardInfo} ${classes.cardItem}`}>
                    <div className={classes.cardInfoWrapper}>
                        <h3>Класс опоры</h3>
                        <span>{props.objects}</span>
                    </div>
                    <div className={classes.cardInfoWrapper}>
                        <h3>ID</h3>
                        <span>{props.ID}</span>
                    </div>
                    <div className={classes.cardInfoWrapper}>
                        <h3>Ср. уверенность</h3>
                        <span>{props["avg-conf"]}</span>
                    </div>
                    <div className={classes.cardInfoWrapper}>
                        <h3>Time taken</h3>
                        <span>{props["time-taken"]}ms</span>
                    </div>
                </div>
                <div className={`${classes.cardModes} ${classes.cardItem}`}>
                    <h3>Режимы разметки</h3>
                    <span>
                        Слайдер, разметка прямоугольниками, разметка с
                        подписями,стоковое фото
                    </span>
                    <div className={classes.buttonsWrapper}>
                        <IconButton
                            icon={
                                <svg
                                    width="24"
                                    height="24"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    xmlns="http://www.w3.org/2000/svg"
                                >
                                    <g clip-path="url(#clip0_2074_2883)">
                                        <path
                                            d="M16.02 12.0001L21.5 15.1301C21.6539 15.2174 21.7819 15.3438 21.871 15.4967C21.96 15.6495 22.0069 15.8232 22.0069 16.0001C22.0069 16.177 21.96 16.3508 21.871 16.5036C21.7819 16.6564 21.6539 16.7829 21.5 16.8701L13 21.7401C12.696 21.9157 12.3511 22.0081 12 22.0081C11.6489 22.0081 11.304 21.9157 11 21.7401L2.49999 16.8701C2.34609 16.7829 2.21808 16.6564 2.12902 16.5036C2.03997 16.3508 1.99304 16.177 1.99304 16.0001C1.99304 15.8232 2.03997 15.6495 2.12902 15.4967C2.21808 15.3438 2.34609 15.2174 2.49999 15.1301L7.97999 12.0001M13 13.7401C12.696 13.9157 12.3511 14.0081 12 14.0081C11.6489 14.0081 11.304 13.9157 11 13.7401L2.49999 8.87014C2.34609 8.78292 2.21808 8.65644 2.12902 8.5036C2.03997 8.35076 1.99304 8.17703 1.99304 8.00014C1.99304 7.82324 2.03997 7.64951 2.12902 7.49667C2.21808 7.34383 2.34609 7.21735 2.49999 7.13014L11 2.26014C11.304 2.0846 11.6489 1.99219 12 1.99219C12.3511 1.99219 12.696 2.0846 13 2.26014L21.5 7.13014C21.6539 7.21735 21.7819 7.34383 21.871 7.49667C21.96 7.64951 22.0069 7.82324 22.0069 8.00014C22.0069 8.17703 21.96 8.35076 21.871 8.5036C21.7819 8.65644 21.6539 8.78292 21.5 8.87014L13 13.7401Z"
                                            stroke="#2D2D2D"
                                            stroke-width="2"
                                            stroke-linecap="round"
                                            stroke-linejoin="round"
                                        />
                                    </g>
                                    <defs>
                                        <clipPath id="clip0_2074_2883">
                                            <rect
                                                width="24"
                                                height="24"
                                                fill="white"
                                            />
                                        </clipPath>
                                    </defs>
                                </svg>
                            }
                            isActive={currentTab == "COMPARE" ? true : false}
                            onClick={() => setCurrentTab("COMPARE")}
                        />
                        <IconButton
                            icon={
                                <svg
                                    width="24"
                                    height="24"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    xmlns="http://www.w3.org/2000/svg"
                                >
                                    <path
                                        d="M16 2H8C6.89543 2 6 2.89543 6 4V20C6 21.1046 6.89543 22 8 22H16C17.1046 22 18 21.1046 18 20V4C18 2.89543 17.1046 2 16 2Z"
                                        stroke="#A6A6A6"
                                        stroke-width="2"
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                    />
                                </svg>
                            }
                            isActive={currentTab == "RECTANGLES" ? true : false}
                            onClick={() => setCurrentTab("RECTANGLES")}
                        />
                        <IconButton
                            icon={
                                <svg
                                    width="24"
                                    height="24"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    xmlns="http://www.w3.org/2000/svg"
                                >
                                    <path
                                        d="M3 7V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H7M17 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V7M21 17V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H17M7 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V17M7 8H15M7 12H17M7 16H13"
                                        stroke="#A6A6A6"
                                        stroke-width="2"
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                    />
                                </svg>
                            }
                            isActive={currentTab == "TEXT" ? true : false}
                            onClick={() => setCurrentTab("TEXT")}
                        />
                        <IconButton
                            icon={
                                <svg
                                    width="24"
                                    height="24"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    xmlns="http://www.w3.org/2000/svg"
                                >
                                    <path
                                        d="M15 3V7C15 7.53043 15.2107 8.03914 15.5858 8.41421C15.9609 8.78929 16.4696 9 17 9H21M16 3H5C4.46957 3 3.96086 3.21071 3.58579 3.58579C3.21071 3.96086 3 4.46957 3 5V19C3 19.5304 3.21071 20.0391 3.58579 20.4142C3.96086 20.7893 4.46957 21 5 21H19C19.5304 21 20.0391 20.7893 20.4142 20.4142C20.7893 20.0391 21 19.5304 21 19V8L16 3Z"
                                        stroke="#A6A6A6"
                                        stroke-width="2"
                                        stroke-linecap="round"
                                        stroke-linejoin="round"
                                    />
                                </svg>
                            }
                            isActive={currentTab == "STOCK" ? true : false}
                            onClick={() => setCurrentTab("STOCK")}
                        />
                    </div>
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
