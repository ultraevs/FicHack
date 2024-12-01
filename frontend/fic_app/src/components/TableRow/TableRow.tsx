import { FC } from "react";
import classes from "./TableRow.module.css";
import StateLabel from "../StateLabel/StateLabel";
import { State } from "../StateLabel/StateLabel";

export interface RawsData {
    avgConf: number;
    objects: string;
    timeTaken: number | string;
}

export interface TableRowProps {
    isHead?: boolean;
    state: State;
    nameOfFile?: string;
    data?: RawsData;
}

const TableRow: FC<TableRowProps> = ({ isHead, state, data, nameOfFile }) => {
    function getFormattedDate(): string {
        const date = new Date();
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
    return (
        <div className={classes.row}>
            <span>ID 3210</span>
            <StateLabel state={state} />
            <span>{nameOfFile}</span>
            <span>{data?.objects}</span>
            <span>{getFormattedDate()}</span>
        </div>
    );
};

export default TableRow;
