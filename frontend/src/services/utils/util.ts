import {RegisterData} from "../api.service.ts";

export function buildRegisterForm(data: RegisterData): FormData {
  const formData = new FormData();

  formData.append("email", data.email);
  formData.append("password", data.password);
  formData.append("user.name", data.user.name);
  formData.append("user.surname", data.user.surname);
  formData.append("user.image", data.user.image); // Важливо: image має бути саме типу File

  return formData;
}
