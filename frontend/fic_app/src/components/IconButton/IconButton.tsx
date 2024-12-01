import React, { FC, ReactNode } from "react";
import classes from "./IconButton.module.css";

interface IconButtonProps {
    icon: ReactNode;
    isActive?: boolean;
    onClick?: (event?: React.MouseEvent<HTMLButtonElement>) => void;
}

const IconButton: FC<IconButtonProps> = ({ icon, isActive, onClick }) => {
    return (
        <button
            type="button"
            onClick={onClick}
            className={`${classes.button} ${isActive ? classes.active : ""}`}
        >
            {icon}
        </button>
    );
};

export default IconButton;
