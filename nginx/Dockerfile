FROM nginx:stable-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY .htpasswd /etc/nginx/.htpasswd
COPY index.html /usr/share/nginx/html/index.html
COPY 401.html /usr/share/nginx/html/401.html


EXPOSE 8198

CMD ["nginx", "-g", "daemon off;"]