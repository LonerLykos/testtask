export const AppRoutes = {
    root: '/',
    register: '/register',
    users: {
        all: '/users',
        create() {
            return `${this.all}/create`
        },
        update(){
            return `${this.all}/:pk`
        },
    },
    filter: '/filter',
    auth: {
        login: '/auth/login',
    }
};