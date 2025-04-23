import {zod} from "../../../zodAlias.ts";


const emailRegex = /^[a-zA-Z0-9_.]+@[a-z0-9]+\.[a-z]+$/;
const passwordRegex = /^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^\w\s:])(\S){8,16}$/;

const registerSchema = zod.object({
    email: zod
        .string()
        .regex(emailRegex, 'Invalid email format')
        .min(1, 'Email is required'),

    password: zod
        .string()
        .regex(passwordRegex, 'Password must be at least 8-16 characters long and contain one uppercase letter, one digit')
        .min(1, 'Password is required'),

    profile: zod.object({
        name: zod
            .string()
            .min(1, 'Name is required')
            .regex(/^[A-Z][a-z]{1,15}$/, 'Name can only contain letters'),

        surname: zod
            .string()
            .min(1, 'Surname is required')
            .regex(/^[A-Z][a-z]{1,15}$/, 'Surname can only contain letters'),

        age: zod
            .coerce.number()
            .min(1, 'Age must be at least 1')
            .max(100, 'Age must be at most 100'),
    }),
});

export default registerSchema;
