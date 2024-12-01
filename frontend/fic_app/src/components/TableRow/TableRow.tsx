import { FC } from "react";
import classes from "./TableRow.module.css";
import StateLabel from "../StateLabel/StateLabel";
import { State } from "../StateLabel/StateLabel";
import trashIcon from "../../assets/images/trash.svg";

export interface RawsData {
    avgConf?: number;
    objects?: string;
    timeTaken?: number | string;
    date?: string;
}

export interface TableRowProps {
    isHead?: boolean;
    isWithDelete?: boolean;
    state: State;
    nameOfFile?: string;
    data?: RawsData;
    id?: number;
}

const TableRow: FC<TableRowProps> = ({
    isHead,
    state,
    data,
    nameOfFile,
    isWithDelete,
    id,
}) => {
    function getFormattedDate(argDate?: string): string {
        let date;
        if (!argDate) {
            date = new Date();
        } else {
            date = new Date(argDate);
        }
        const months = [
            "янв",
            "фев",
            "мар",
            "апр",
            "мая",
            "июн",
            "июл",
            "авг",
            "сент",
            "окт",
            "нояб",
            "дек",
        ];

        const day = date.getDate();
        const month = months[date.getMonth()];
        const hours = date.getHours().toString().padStart(2, "0");
        const minutes = date.getMinutes().toString().padStart(2, "0");
        return `${day} ${month}. ${hours}:${minutes}`;
    }
    if (isHead) {
        return (
            <div className={classes.headRow}>
                <span>ID</span>
                <span>Имя файла</span>
                <span>Класс опоры</span>
                <span>Дата</span>
            </div>
        );
    }
    if (isWithDelete) {
        return (
            <div className={classes.withDeleteRow}>
                <span>ID 3210</span>
                <StateLabel state={state} />
                <span>{nameOfFile}</span>
                <span>{data?.objects}</span>
                {data?.date ? (
                    <span>{getFormattedDate(data?.date)}</span>
                ) : (
                    <span>{getFormattedDate()}</span>
                )}
                <button type="button">
                    <img src={trashIcon} />
                </button>
            </div>
        );
    }
    return (
        <div className={classes.row}>
            <span>ID {id}</span>
            <StateLabel state={state} />
            <span>{nameOfFile}</span>
            <span>{data?.objects}</span>
            {data?.date ? (
                <span>{getFormattedDate(data?.date)}</span>
            ) : (
                <span>{getFormattedDate()}</span>
            )}
        </div>
    );
};

export default TableRow;
