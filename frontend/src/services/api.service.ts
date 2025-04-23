import axios from 'axios';
import {baseUrl} from "../constants/urls.ts";
import Cookies from "js-cookie";
import {ITokenPair} from "../models/token-model/ITokenModel.ts";

export type RegisterData = {
    email: string;
    password: string;
    user: {
        name: string,
        surname: string,
        image: File,
    }
}

export type LoginData = {
    email: string;
    password: string;
}

export const axiosInstance = axios.create({
    baseURL: baseUrl,
    headers: {'Content-Type': 'application/json'},
});

axiosInstance.interceptors.request.use(req => {
    const cookie = Cookies.get('token');
    if (cookie) {
        const token: ITokenPair = JSON.parse(cookie);
        req.headers.Authorization = `Bearer ${token.access}`;
    }
    return req;
})