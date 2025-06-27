import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

export const fetchProducts = async (filters) => {
  const response = await axios.get(`${API_URL}/products/`, { params: filters });
  return response.data;
};

export const fetchCategories = async () => {
  const response = await axios.get(`${API_URL}/categories/`);
  return response.data;
};
