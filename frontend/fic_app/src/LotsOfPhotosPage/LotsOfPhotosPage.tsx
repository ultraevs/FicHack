import { useState } from "react";
import classes from "./LotsOfPhotosPage.module.css";
import TableRow from "../components/TableRow/TableRow";
const LotsOfPhotosPage = () => {
    const [qtyOfPhotos, setQtyOfPhotos] = useState<number>(20);
    return (
        <section className={classes.LotsOfPhotosPage}>
            <div className="container">
                <div className={classes.textBlock}>
                    <h3>Всего {qtyOfPhotos} фото</h3>
                    <span>Все изображения перемещены в историю обработок</span>
                    <div className={classes.tableWrapper}>
                        <TableRow isHead={true} />
                    </div>
                </div>
            </div>
        </section>
    );
};

export default LotsOfPhotosPage;
