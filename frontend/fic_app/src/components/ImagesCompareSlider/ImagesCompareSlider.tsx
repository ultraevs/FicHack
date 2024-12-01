import React, { FC } from "react";
import ReactCompareImage from "react-compare-image";

interface ImagesCompareSliderProps {
    leftImage: string;
    rightImage: string;
}

const ImagesCompareSlider: FC<ImagesCompareSliderProps> = ({
    leftImage,
    rightImage,
}) => {
    return (
        <ReactCompareImage
            leftImage={leftImage}
            rightImage={rightImage}
            handle={<React.Fragment />}
            sliderLineWidth={8}
        />
    );
};

export default ImagesCompareSlider;
