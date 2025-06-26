import { createContext } from 'react';
import { ClientSideContextInterface } from './client_types';

export const ClientSideContext = createContext<ClientSideContextInterface>(null);;
