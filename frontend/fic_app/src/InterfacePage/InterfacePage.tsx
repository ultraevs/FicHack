import { useState, useCallback } from "react";
import Dropzone from "react-dropzone";
import Button from "../components/Button/Button";
import PhotoInformationCard from "../components/PhotoInformationCard/PhotoInformationCard";
import classes from "./InterfacePage.module.css";

const InterfacePage = () => {
    const [imagePreview, setImagePreview] = useState<string | null>(null);

    const onDrop = useCallback((acceptedFiles: File[]) => {
        const file = acceptedFiles[0];
        if (file) {
            const previewUrl = URL.createObjectURL(file);
            setImagePreview(previewUrl);
        }
    }, []);

    return (
        <section>
            <div className="container">
                <div className={classes.interfaceWrapper}>
                    <div className={classes.getPhotoWrapper}>
                        {imagePreview ? (
                            <div className={classes.imagePreview}>
                                <img src={imagePreview} alt="Preview" />
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
                                    <div
                                        className={classes.getPhotoBlock}
                                        {...getRootProps()}
                                    >
                                        <input {...getInputProps()} />
                                        Перетащите изображение сюда
                                    </div>
                                )}
                            </Dropzone>
                        )}
                        {imagePreview ? (
                            <Button
                                text="Сбросить"
                                onClick={() => setImagePreview(null)}
                            />
                        ) : (
                            <Button text="+ Добавить фото" />
                        )}
                    </div>
                    <PhotoInformationCard props={null} />
                </div>
            </div>
        </section>
    );
};

export default InterfacePage;
