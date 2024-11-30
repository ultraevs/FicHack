import { useState, useCallback, useRef } from "react";
import Dropzone from "react-dropzone";
import Button from "../components/Button/Button";
import PhotoInformationCard from "../components/PhotoInformationCard/PhotoInformationCard";
import classes from "./InterfacePage.module.css";
import ImagesCompareSlider from "../components/ImagesCompareSlider/ImagesCompareSlider";
import { PhotoInformationCardProps } from "../components/PhotoInformationCard/PhotoInformationCard";
const InterfacePage = () => {
    // УДАЛИТЬ ПОТОМ!!!
    const testData = {
        classOfSupport: "ЛЭП класс 1",
        ID: 3201,
        conf: 0.7,
        time_taken: 100,
    };

    const [imagePreview, setImagePreview] = useState<string | null>(null);
    const [photoInformationProps, setPhotoInformationProps] =
        useState<PhotoInformationCardProps | null>(null);
    const fileInputRef = useRef<HTMLInputElement | null>(null);
    const onDrop = useCallback((acceptedFiles: File[]) => {
        if (acceptedFiles.length > 1) {
            alert(
                "Можно добавить лишь один файл. Если вы хотите добавить больше - перейдите на страницу 'Множество фото'"
            );
            return;
        }
        const file = acceptedFiles[0];
        if (file) {
            const previewUrl = URL.createObjectURL(file);
            setImagePreview(previewUrl);
            setPhotoInformationProps(testData);
        }
    }, []);

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
                                    className={classes.getPhotoBlock}
                                    {...getRootProps()}
                                >
                                    {imagePreview ? (
                                        <div className={classes.imagePreview}>
                                            <ImagesCompareSlider
                                                leftImage={imagePreview}
                                                rightImage={imagePreview}
                                            />
                                            {/* <img
                                                src={imagePreview}
                                                alt="Preview"
                                            /> */}
                                        </div>
                                    ) : (
                                        "Перетащите изображение сюда"
                                    )}
                                </div>

                                <input
                                    {...getInputProps()}
                                    ref={fileInputRef}
                                    style={{ display: "none" }}
                                />

                                {imagePreview ? (
                                    <Button
                                        text="Сбросить"
                                        onClick={() => setImagePreview(null)}
                                    />
                                ) : (
                                    <Button
                                        text="+ Добавить фото"
                                        onClick={() =>
                                            fileInputRef.current?.click()
                                        }
                                    />
                                )}
                            </div>
                        )}
                    </Dropzone>
                    <PhotoInformationCard props={photoInformationProps} />
                </div>
            </div>
        </section>
    );
};

export default InterfacePage;
