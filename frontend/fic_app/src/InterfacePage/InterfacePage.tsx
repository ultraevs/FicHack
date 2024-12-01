import { useState, useCallback, useRef } from "react";
import Dropzone from "react-dropzone";
import Button from "../components/Button/Button";
import PhotoInformationCard from "../components/PhotoInformationCard/PhotoInformationCard";
import classes from "./InterfacePage.module.css";
import ImagesCompareSlider from "../components/ImagesCompareSlider/ImagesCompareSlider";
import { PhotoInformationCardProps } from "../components/PhotoInformationCard/PhotoInformationCard";
import { fetchInfo } from "../Requests/getInfo";
import { useTab } from "../Contexts/TabsContext/TabsContext";

type Image = string;

const InterfacePage = () => {
    const [photoInformationProps, setPhotoInformationProps] =
        useState<PhotoInformationCardProps | null>(null);
    const [imagesList, setImagesList] = useState<Image[] | null>(null);
    const fileInputRef = useRef<HTMLInputElement | null>(null);
    const { currentTab } = useTab();

    const onDrop = useCallback((acceptedFiles: File[]) => {
        if (acceptedFiles.length > 1) {
            alert(
                "Можно добавить лишь один файл. Если вы хотите добавить больше - перейдите на страницу 'Множество фото'"
            );
            return;
        }

        const file = acceptedFiles[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = async () => {
                try {
                    const base64data = reader.result as string;
                    const data = await fetchInfo(base64data);

                    if (
                        data &&
                        Array.isArray(data.results) &&
                        data.results.length > 0
                    ) {
                        setPhotoInformationProps(
                            data
                                .results[0] as unknown as PhotoInformationCardProps
                        );
                        setImagesList(data.results[0].images);
                    }
                } catch (error) {
                    console.error("Ошибка при получении данных:", error);
                }
            };
            reader.onerror = () => console.error("Ошибка при чтении файла");
            reader.readAsDataURL(file);
        }
    }, []);

    const renderTabContent = (images: Image[]) => {
        console.log(images);
        switch (currentTab) {
            case "COMPARE":
                return (
                    <ImagesCompareSlider
                        leftImage={`data:image/png;base64, ${images[3]}`}
                        rightImage={`data:image/png;base64, ${images[0]}`}
                    />
                );
            case "RECTANGLES":
                return (
                    <img
                        src={`data:image/png;base64, ${images[0]}`}
                        className={classes.preview}
                        alt="Rectangles"
                    />
                );
            case "TEXT":
                return (
                    <img
                        src={`data:image/png;base64, ${images[1]}`}
                        className={classes.preview}
                        alt="Text"
                    />
                );
            case "STOCK":
                return (
                    <img
                        src={`data:image/png;base64, ${images[2]}`}
                        className={classes.preview}
                        alt="Stock"
                    />
                );
            default:
                return (
                    <ImagesCompareSlider
                        leftImage={`data:image/png;base64, ${images[3]}`}
                        rightImage={`data:image/png;base64, ${images[0]}`}
                    />
                );
        }
    };

    return (
        <section>
            <div className="container">
                <div className={classes.interfaceWrapper}>
                    <Dropzone
                        onDrop={onDrop}
                        accept={{
                            "image/jpeg": [".jpeg", ".jpg"],
                            "image/png": [".png"],
                        }}
                    >
                        {({ getRootProps, getInputProps }) => (
                            <div className={classes.getPhotoWrapper}>
                                <div
                                    className={`${classes.getPhotoBlock} ${
                                        imagesList
                                            ? classes.getPhotoBlockWithoutBG
                                            : ""
                                    }`}
                                    {...getRootProps()}
                                >
                                    {imagesList
                                        ? renderTabContent(imagesList || [])
                                        : "Перетащите изображение сюда"}
                                </div>
                                <input
                                    {...getInputProps()}
                                    ref={fileInputRef}
                                    style={{ display: "none" }}
                                />
                                <Button
                                    text={
                                        imagesList
                                            ? "Сбросить"
                                            : "+ Добавить фото"
                                    }
                                    onClick={() =>
                                        imagesList
                                            ? resetState()
                                            : fileInputRef.current?.click()
                                    }
                                />
                            </div>
                        )}
                    </Dropzone>
                    <PhotoInformationCard props={photoInformationProps} />
                </div>
            </div>
        </section>
    );

    function resetState() {
        setImagesList(null);
        setPhotoInformationProps(null);
        setImagesList(null);
    }
};

export default InterfacePage;
