import { FC, ReactNode } from "react";
import classes from "./Button.module.css";

type Theme = "ghost" | "default";

interface ButtonProps {
    text: string;
    isActive?: boolean;
    theme?: Theme;
    onClick?: (event?: React.MouseEvent<HTMLButtonElement>) => void;
    children?: ReactNode;
}

const Button: FC<ButtonProps> = ({
    text,
    isActive,
    theme = "default",
    onClick,
    children,
}) => {
    const buttonClass = `${classes.button} ${isActive ? classes.active : ""} ${
        classes[theme]
    }`;
    return (
        <button type="button" className={buttonClass} onClick={onClick}>
            {text}
            {children}
        </button>
    );
};

export default Button;
