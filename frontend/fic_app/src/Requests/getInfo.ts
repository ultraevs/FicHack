import axios from "axios";
import { PhotoInformationCardProps } from "../components/PhotoInformationCard/PhotoInformationCard";

export const fetchInfo = async (
    data_base64: string
): Promise<{ results: PhotoInformationCardProps } | null> => {
    try {
        const response = await axios.post(
            "http://77.37.181.114:8100/process_base64/",
            {
                data: [data_base64],
            }
        );
        console.log(response);
        return response.data;
    } catch (error) {
        console.error("Error:", error);
        return null;
    }
};
