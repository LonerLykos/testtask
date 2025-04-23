export interface IUser {
  id: number;
  name: string;
  surname: string;
  rank: null|number;
  avatar: string;
}

export interface IProfile {
  id: number;
  email: string;
  is_active: boolean;
  is_staff: boolean;
  user: IUser;
  created_at: string;
  updated_at: string;
}