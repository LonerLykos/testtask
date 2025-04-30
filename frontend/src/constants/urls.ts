export const baseUrl = '/api'

export const urls = {
    auth: {
        login: '/auth',
    },
    users: {
        all: '/users',
        create() {
            return `${this.all}/create`
        },
        certificate(pk:string){
            return `${this.all}/${pk}/certificate`
        }
    }

};
