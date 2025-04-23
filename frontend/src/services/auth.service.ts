import {urls} from "../constants/urls.ts";
import Cookies from "js-cookie";
import {axiosInstance, LoginData} from "./api.service.ts";

export const authService = {
    async login(loginData: LoginData) {
        const {data} = await axiosInstance.post(urls.auth.login, loginData);
        Cookies.set('token', JSON.stringify(data));
        return data;
    },

}


