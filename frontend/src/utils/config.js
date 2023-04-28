export const endpoint = "http://127.0.0.1:8000/api";

// Configuração para as requisições HTTP

export const requestConfig = (method, data, token = null) => {
  let config;

  config = {
      method,
      body: JSON.stringify(data),
      headers: { "Content-Type": "application/json" },
    };
  

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
};
