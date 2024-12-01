import { FC } from "react";
import classes from "./TableRow.module.css";
interface TableRowProps {
    isHead?: boolean;
}

const TableRow: FC<TableRowProps> = ({ isHead }) => {
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
    return <div></div>;
};

export default TableRow;
