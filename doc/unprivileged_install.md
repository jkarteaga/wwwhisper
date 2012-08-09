### Install required packages.

    sudo apt-get install git python python-dev python-virtualenv libssl-dev libpcre3;

### Get, compile and install nginx.
    # Download and unpack the latest stable nginx.
    mkdir -p ~/src; cd ~/src;
    NGINX_VERSION='nginx-1.2.3';
    wget http://nginx.org/download/${NGINX_VERSION}.tar.gz;
    tar xvfz ${NGINX_VERSION}.tar.gz;
    cd ${NGINX_VERSION};
    # Get auth-request module.
    git clone https://github.com/PiotrSikora/ngx_http_auth_request_module.git;
    # Configure nginx. If your site needs any additonal modules add them here.
    ./configure --add-module=./ngx_http_auth_request_module/ \
      --with-http_ssl_module --with-http_sub_module --prefix=$HOME/local/nginx/
    # Compile and install nginx.
    make; make install;

### Install wwwhispers.
    # Choose where to put wwwhisper files.
    cd ~/local;
    git clone https://github.com/wrr/wwwhisper.git; cd wwwhisper;
    # Create and activate virtual environment.
    virtualenv virtualenv;
    source virtualenv/bin/activate;
    # Install required packages in the virtual environment.
    pip install -r ./requirements.txt;
    # Generate configurations files for a site to protect. You need to
    # specify your email as admin_email to be able to access the
    # admin web application. This step can be later repeated to enable
    # protection for multiple sites.
    ./add_site_config.py --site-url  http[s]://your.domain[:port] --admin-email your@email;

### Configure nginx.

Edit ~/local/nginx/conf/nginx.conf and enable wwwhisper
authorization. In the server section put (/home/alice/local/wwwhisper
must be replaced everywhere with a path where wwwhisper is installed):

    set $wwwhisper_root /home/alice/local/wwwhisper;
    set $wwwhisper_site_socket unix:$wwwhisper_root/sites/$scheme.$server_name.$server_port/uwsgi.sock;
    include /home/alice/local/wwwhisper/nginx/auth.conf;

In each location section that requires protection and that is not nested in already protected location put:

    include /home/alice/local/wwwhisper/nginx/protected_location.conf;

To enable the admin application, in the root location put:

    include /home/alice/local/wwwhisper/nginx/admin.conf;

See [a sample configuration
file](https://github.com/wrr/wwwhisper/blob/master/nginx/sample_nginx.conf)
for a more detailed explaination of all wwwhisper related configuration
directives.

### Start nginx and wwwhisper.
    ~/local/bin/nginx;
    cd ~/local/wwwhisper; source virtualenv/bin/activate;
    ./run_wwwhisper_for_site.sh -d sites/http[s].your.domain.port

Point your browser to http[s]://your.domain[:port]/admin, you should be
presented with a login page. Sign in with your email and use the admin
application to define which locations can be accessed by which
visitors.