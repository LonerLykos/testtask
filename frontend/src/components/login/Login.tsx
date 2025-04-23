import {useForm} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import {LoginData} from "../../services/api.service.ts";
import loginSchema from "../validator/login.validator.ts";
import {authService} from "../../services/auth.service.ts";
// import {useNavigate} from "react-router-dom";


export const Login = () => {

    // const navigate = useNavigate();

    const {handleSubmit, register, formState: {errors, isValid}, reset} =
        useForm<LoginData>({
            mode: 'all',
            resolver: zodResolver(loginSchema),
        });

    const myHandler = async (data: LoginData) => {
        try {
            const token = await authService.login(data)
            console.log(token);
            // if (token) {
            //     navigate('/pizzas');
            // }

            reset();

        } catch (error) {
            console.log(error)
            reset();
        }
    }

    return (
        <div>
            <h1>Sing up</h1>
            <form onSubmit={handleSubmit(myHandler)}>
                <div className='wrap-input'>
                    <label>
                        <input type="text" placeholder="example@mail.com" {...register('email')}/>
                    </label>

                    <p className={!errors.email ? 'hide' : 'view'}>{!errors.email ? '' : errors.email.message}</p>
                </div>
                <div className='wrap-input'>
                    <label>
                        <input type="text" placeholder="Enter your password" {...register('password')}/>
                    </label>

                    <p className={!errors.password ? 'hide' : 'view'}>{!errors.password ? '' : errors.password.message}</p>
                </div>

                <button disabled={!isValid}>Register</button>
            </form>
        </div>
    );
};
