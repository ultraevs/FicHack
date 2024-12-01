import axios from "axios";
import { PhotoInformationCardProps } from "../components/PhotoInformationCard/PhotoInformationCard";
axios.defaults.withCredentials = true;
export const fetchInfo = async (
    data_base64: string,
    name: string
): Promise<{ results: PhotoInformationCardProps } | null> => {
    try {
        const response = await axios.post(
            "http://localhost:8200/process_base64/",
            {
                data: [data_base64],
                file_name: name,
            }
        );
        console.log(response);
        return response.data;
    } catch (error) {
        console.error("Error:", error);
        return null;
    }
};

export const fetchLogin = async (
    login: string,
    password: string
): Promise<boolean> => {
    try {
        const response = await axios.post(
            "http://localhost:8200/login/",
            {
                username: login,
                password: password,
            },
            {
                withCredentials: true,
            }
        );
        console.log("Login response: ", response);
        if (response.status == 200) {
            const user_id = response.data.id;
            setUserIdCookie(user_id);
        } else return false;
    } catch (error) {
        console.error("Error:", error);
        return false;
    }
};

export const fetchRegister = async (
    login: string,
    password: string
): Promise<boolean> => {
    try {
        const response = await axios.post(
            "http://localhost:8200/register/",
            {
                username: login,
                password: password,
            },
            {
                withCredentials: true,
            }
        );
        console.log("Register response: ", response);
        if (response.status == 200) {
            const user_id = response.data.id;
            setUserIdCookie(user_id);
            return true;
        } else return false;
    } catch (error) {
        console.error("Error:", error);
        return false;
    }
};

export const fetchHistory = async (): Promise<boolean> => {
    try {
        const response = await axios.get(
            "http://localhost:8200/user_history/",
            {
                withCredentials: true,
            }
        );
        if (response.status == 200) {
            console.log(response.data.history);
            return response.data.history;
        } else return false;
    } catch (error) {
        console.error("Error:", error);
        return false;
    }
};

function setUserIdCookie(userID: string): void {
    const cookieName = "user_id";
    const cookieValue = userID;
    const expirationDays = 7;

    const date = new Date();
    date.setTime(date.getTime() + expirationDays * 24 * 60 * 60 * 1000);
    const expires = "expires=" + date.toUTCString();

    document.cookie = `${cookieName}=${cookieValue}; ${expires}; path=/`;
}

function getCookie(name: string): string | null {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()?.split(";").shift();
    return null;
}
