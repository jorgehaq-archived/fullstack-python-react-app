
FROM node:18-alpine as builder

WORKDIR /app

# Copiar archivos de configuración
COPY package.json package-lock.json* ./

# Instalar dependencias
RUN npm ci || npm install

# Copiar el código fuente
COPY . .

# Construir la aplicación
RUN npm run build

# Etapa de producción
FROM nginx:alpine

# Copiar la configuración de nginx personalizada si es necesaria
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copiar los archivos de construcción desde la etapa anterior
COPY --from=builder /app/build /usr/share/nginx/html

# Exponer el puerto 80
EXPOSE 80

# Iniciar nginx
CMD ["nginx", "-g", "daemon off;"]
