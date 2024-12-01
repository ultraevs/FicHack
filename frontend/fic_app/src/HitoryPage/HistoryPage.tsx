import { useEffect, useState } from "react";
import TableRow from "../components/TableRow/TableRow";
import classes from "./HistoryPage.module.css";
import { fetchHistory } from "../Requests/getInfo";

const HistoryPage = () => {
    const [history, editHistory] = useState([]);

    useEffect(() => {
        fetchHistory(editHistory);
    }, []);

    return (
        <section className={classes.history}>
            <div className="container">
                <h3>История обработок</h3>
                <div className={classes.historyTable}>
                    <TableRow isHead={true} state="SUCCESS" />
                    {history.map((item, i) => (
                        <TableRow
                            state={"SUCCESS"}
                            data={item["created_at"]}
                            isWithDelete={true}
                            id={item["ID"]}
                            nameOfFile={item["file_name"]}
                            key={i}
                        />
                    ))}
                </div>
            </div>
        </section>
    );
};

export default HistoryPage;
