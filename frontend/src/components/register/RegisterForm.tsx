import registerSchema from "../validator/register.validator.ts";
import {zodResolver} from "@hookform/resolvers/zod";
import {useForm} from "react-hook-form";
import {useState} from "react";
import {registerUser} from "../../services/profile.service.ts";
import {useNavigate} from "react-router-dom";

interface RegInput {
    email: string,
    password: string,
    user: {
        name: string,
        surname: string,
        image: FileList,
    };
}

export const RegisterForm = () => {

    const [stat, setStat] = useState<number>(0)
    const navigate = useNavigate()

    const {handleSubmit, register, formState: {errors, isValid}, reset} =
        useForm<RegInput>({
            mode: 'all',
            resolver: zodResolver(registerSchema),
        });

    const myHandler = async (data: RegInput) => {
        const {email, password, user} = data
        const {name, surname, image} = user
        const file = image[0]
        const regData = {
            email: email,
            password: password,
            user: {
                name: name,
                surname: surname,
                image: file
            }
        }
        try {
            const status = await registerUser(regData)

            if (status === 201) {
                navigate('/')
            }
            reset()
        } catch (e) {
            console.log(e)
            setStat(1)
            reset()
        }
    }

    return (
        <div>
            {stat !== 2 &&
                <>
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
                    <div className='wrap-input'>
                        <label>
                            <input type="text" placeholder='Your name' {...register('user.name')}/>
                        </label>

                        <p className={!errors.user?.name ? 'hide' : 'view'}>{!errors.user?.name ? '' : errors.user?.name.message}</p>
                    </div>
                    <div className='wrap-input'>
                        <label>
                            <input type="text" placeholder='Your surname' {...register('user.surname')}/>
                        </label>

                        <p className={!errors.user?.surname ? 'hide' : 'view'}>{!errors.user?.surname ? '' : errors.user?.surname.message}</p>
                    </div>
                    <div className='wrap-input'>
                        <label>
                            <input type="file" placeholder='Put your photo' {...register('user.image')}/>
                        </label>

                        <p className={!errors.user?.image ? 'hide' : 'view'}>{!errors.user?.image ? '' : errors.user?.image.message}</p>
                    </div>

                    <button disabled={!isValid}>Register</button>
                </form>
                </>
            }
        </div>
    );
};
