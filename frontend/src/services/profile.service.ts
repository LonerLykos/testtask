import {urls} from "../constants/urls.ts";
import {axiosInstance, RegisterData} from "./api.service.ts";


export const UsersService = {
    async get_all() {
        const {data} = await axiosInstance.get(urls.users.all);
        return data
    },

}

export const registerUser = async (regData: RegisterData) => {
    const axiosResponse = await axiosInstance.post('/users/create', regData);
    return axiosResponse;
}

