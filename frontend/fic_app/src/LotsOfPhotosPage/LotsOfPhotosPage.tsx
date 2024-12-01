import { useCallback, useState } from "react";
import classes from "./LotsOfPhotosPage.module.css";
import TableRow from "../components/TableRow/TableRow";
import Dropzone from "react-dropzone";
import { fetchInfo } from "../Requests/getInfo";
import { TableRowProps } from "../components/TableRow/TableRow";

const LotsOfPhotosPage = () => {
    type RawsDataMap = Map<number, TableRowProps>;

    const [qtyOfPhotos, setQtyOfPhotos] = useState<number | null>(null);
    const [werePhotosUploaded, setWerePhotosUploaded] =
        useState<boolean>(false);
    const [rawsData, setRawsData] = useState<RawsDataMap>(new Map());

    const onDrop = useCallback((acceptedFiles: File[]) => {
        if (acceptedFiles.length === 0) {
            console.error("Нет загруженных файлов");
            return;
        }

        setQtyOfPhotos(acceptedFiles.length);
        setWerePhotosUploaded(true);

        acceptedFiles.forEach((file, i) => {
            const reader = new FileReader();
            reader.onloadend = async () => {
                try {
                    const base64data = reader.result as string;
                    const data = await fetchInfo(base64data, file.name);

                    setRawsData((prevRawsData) => {
                        const updatedRawsData = new Map(prevRawsData);
                        const formattedData = data?.results[0];
                        try {
                            if (formattedData.objects.length < 1) {
                                updatedRawsData.set(i, {
                                    state: "ERROR",
                                    nameOfFile: file.name,
                                    data: {
                                        avgConf: -1,
                                        objects: "Не распознано",
                                        timeTaken: -1,
                                    },
                                });
                            } else {
                                updatedRawsData.set(i, {
                                    state: "SUCCESS",
                                    nameOfFile: file.name,
                                    data: {
                                        avgConf: formattedData["avg-conf"],
                                        objects: formattedData.objects,
                                        timeTaken: formattedData["time-taken"],
                                    },
                                });
                            }
                        } catch {
                            updatedRawsData.set(i, {
                                state: "ERROR",
                                nameOfFile: file.name,
                                data: {
                                    avgConf: -1,
                                    objects: "",
                                    timeTaken: -1,
                                },
                            });
                        }
                        return updatedRawsData;
                    });
                } catch (error) {
                    console.error("Ошибка при получении данных:", error);
                }
            };
            reader.onerror = () => console.error("Ошибка при чтении файла");
            reader.readAsDataURL(file);

            setRawsData((prevRawsData) => {
                const updatedRawsData = new Map(prevRawsData);
                updatedRawsData.set(i, {
                    state: "LOADING",
                    nameOfFile: file.name,
                    data: {
                        avgConf: 0,
                        objects: "",
                        timeTaken: 0,
                    },
                });
                return updatedRawsData;
            });
        });
    }, []);

    return (
        <section className={classes.LotsOfPhotosPage}>
            <div className="container">
                {werePhotosUploaded ? (
                    <div className={classes.textBlock}>
                        <h3>Всего {qtyOfPhotos} фото</h3>
                        <span>
                            Все изображения перемещены в историю обработок
                        </span>
                        <div className={classes.tableWrapper}>
                            <TableRow isHead={true} state="SUCCESS" />
                            {Array.from(rawsData.entries()).map(
                                ([key, item]) => (
                                    <TableRow
                                        key={key}
                                        state={item.state}
                                        data={item.data}
                                        nameOfFile={item.nameOfFile}
                                    />
                                )
                            )}
                        </div>
                    </div>
                ) : (
                    <Dropzone
                        onDrop={onDrop}
                        accept={{
                            "image/jpeg": [".jpeg", ".jpg"],
                            "image/png": [".png"],
                        }}
                    >
                        {({ getRootProps, getInputProps }) => (
                            <>
                                <div
                                    className={classes.getPhotoBlock}
                                    {...getRootProps()}
                                >
                                    <span>
                                        Перетащите несколько изображений в это
                                        окно
                                    </span>
                                </div>
                                <input {...getInputProps()} />
                            </>
                        )}
                    </Dropzone>
                )}
            </div>
        </section>
    );
};

export default LotsOfPhotosPage;
