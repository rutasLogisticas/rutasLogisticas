# Dockerfile para Frontend Angular
FROM node:20-alpine

# Configurar variables de entorno para UTF-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm ci

# Copiar el resto del código
COPY . .

# Exponer puerto
EXPOSE 4200

# Comando para desarrollo con hot-reload
CMD ["npm", "start", "--", "--host", "0.0.0.0", "--poll", "2000"]

