import {urls} from "../constants/urls.ts";
import {axiosInstance, RegisterData} from "./api.service.ts";
import {buildRegisterForm} from "./utils/util.ts";


export const ProfileService = {
    async get_all() {
        const {data} = await axiosInstance.get(urls.users.all);
        return data
    },

}

export const registerUser = async (regData: RegisterData):Promise<number|void> => {

    const formData = buildRegisterForm(regData);

    try {
        const {status} = await axiosInstance.post('/users/create', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });

        return status;
    } catch (error) {
        console.error( error);
    }
}

