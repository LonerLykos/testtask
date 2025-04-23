import {zod} from "../../../zodAlias.ts";


const emailRegex = /^[a-zA-Z0-9_.]+@[a-z0-9]+\.[a-z]+$/;
const passwordRegex = /^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^\w\s:])(\S){3,16}$/;

const registerSchema = zod.object({
    email: zod
        .string()
        .regex(emailRegex, 'Invalid email format')
        .min(1, 'Email is required'),

    password: zod
        .string()
        .regex(passwordRegex, 'Password must be at least 8-16 characters long and contain one uppercase letter, one digit')
        .min(1, 'Password is required'),

    user: zod.object({
        name: zod
            .string()
            .min(1, 'Name is required')
            .regex(/^[A-Z][a-z]{1,15}$/, 'Name can only contain letters'),

        surname: zod
            .string()
            .min(1, 'Surname is required')
            .regex(/^[A-Z][a-z]{1,15}$/, 'Surname can only contain letters'),

        image: zod
            .instanceof(FileList)
            .superRefine((fileList, ctx) => {
                if (fileList.length === 0) {
                    ctx.addIssue({
                        code: zod.ZodIssueCode.custom,
                        message: 'You must upload a file',
                        path: ['image'],
                    });
                } else {
                    const file = fileList[0];
                    if (file.size > 5 * 1024 * 1024) {
                        ctx.addIssue({
                            code: zod.ZodIssueCode.custom,
                            message: 'File size must be less than 5MB',
                            path: ['image'],
                        });
                    }
                    if (!file.type.startsWith('image/')) {
                        ctx.addIssue({
                            code: zod.ZodIssueCode.custom,
                            message: 'File must be an image',
                            path: ['image'],
                        });
                    }
                }
            }),
    }),
});

export default registerSchema;
