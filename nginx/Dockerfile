FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY https-nginx.conf /etc/nginx/conf.d

COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]