import {urls} from "../constants/urls.ts";
// import Cookies from "js-cookie";
import {axiosInstance, LoginData, RegisterData} from "./api.service.ts";

export const authService = {
    async login(loginData: LoginData) {
        const res = await axiosInstance.post(urls.auth.login, loginData);
        console.log(res);
        return res
        // Cookies.set('token', JSON.stringify(data));
        // return data;
    },

}

export const registerUser = async (regData: RegisterData) => {
    const axiosResponse = await axiosInstance.post('/users', regData);
    return axiosResponse;
}

