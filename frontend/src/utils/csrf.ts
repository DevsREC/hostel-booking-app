import { api } from "@/action/user";

export const fetchCSRFToken = async () => {
    try {
        await api.get('/csrf/');
        return true;
      } catch (error) {
        console.error('Failed to fetch CSRF token:', error);
        return false;
      }
}

export const setupCSRF = () => {
    api.interceptors.request.use(config => {
      const csrfToken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
      
      if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken;
      }
      
      return config;
    });
  };
  