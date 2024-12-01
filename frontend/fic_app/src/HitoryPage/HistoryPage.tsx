import { useEffect } from "react";
import TableRow from "../components/TableRow/TableRow";
import classes from "./HistoryPage.module.css";
import { fetchHistory } from "../Requests/getInfo";
const HistoryPage = () => {
    useEffect(() => {
        fetchHistory();
    }, []);
    return (
        <section className={classes.history}>
            <div className="container">
                <h3>История обработок</h3>
                <div className={classes.historyTable}>
                    <TableRow isHead={true} state="SUCCESS" />
                    <TableRow
                        state={"ERROR"}
                        data={{ date: "2005-07-18" }}
                        isWithDelete={true}
                    />
                </div>
            </div>
        </section>
    );
};

export default HistoryPage;
