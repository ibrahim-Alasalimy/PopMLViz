from flask import jsonify, request, send_file
from .app import create_app
import pandas as pd
import json
from sklearn.decomposition import PCA
import random, string
from .common import runKmeans
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import os
import rpy2.robjects as robjects
from fcmeans import FCM
from sklearn.ensemble import IsolationForest
import pickle
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from sklearn.cluster import AgglomerativeClustering 
from sklearn.covariance import EllipticEnvelope
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from flask import Blueprint, make_response
from flask_cors import cross_origin
from flask_bcrypt import Bcrypt
import sqlite3
from flask_jwt_extended import create_access_token,create_refresh_token, get_jwt_identity, jwt_required
from datetime import timedelta
from umap import UMAP
from sklearn.cluster import DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.cluster import SpectralClustering
from sklearn.neighbors import KNeighborsClassifier
from sklearn.covariance import EllipticEnvelope


main_blueprint = Blueprint('main', __name__)
bcrypt = Bcrypt()

# Create an application instance
app = create_app()


# Define a route to fetch the available article
UPLOAD_FOLDER = './data'

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

@app.route("/", methods=["GET"], strict_slashes=False) #2 dummy endpoint
@cross_origin()
def helloWorld():
    return "Hello World"

@app.route("/api/runkmeans", methods=["POST"], strict_slashes=False) #1
@cross_origin() 
def runKmeans():
    request_df = request.get_json()['df']
    num_clusters = request.get_json()['num_clusters']
    if num_clusters < 2:
        num_clusters = 2
    pca_df = pd.json_normalize(request_df)
    try:
        pca_cols = [x for x in pca_df.columns if 'PC' in x or 'TSNE' in x or 'UMAP' in x]
    except:
        pca_cols = pca_df.columns
    
    if not pca_cols:
        pca_cols = pca_df.columns
    kmeans = KMeans(n_clusters=num_clusters, random_state=123).fit_predict(pca_df[pca_cols])
    return jsonify(list(map(lambda x: int(x), kmeans)))

@app.route("/api/runspectral", methods=["POST"], strict_slashes=False)
@cross_origin()
def runSpectral():
    request_df = request.get_json()['df']
    num_clusters = request.get_json().get('num_clusters', 2)
    
    if num_clusters < 2:
        num_clusters = 2
    
    pca_df = pd.json_normalize(request_df)
    try:
        pca_cols = [x for x in pca_df.columns if 'PC' in x or 'TSNE' in x or 'UMAP' in x]
    except:
        pca_cols = pca_df.columns
    
    if not pca_cols:
        pca_cols = pca_df.columns
    
    spectral = SpectralClustering(n_clusters=num_clusters, affinity='nearest_neighbors', random_state=123).fit(pca_df[pca_cols])
    clusters = spectral.labels_
    
    return jsonify({'result': list(map(lambda x: int(x), clusters))})

@app.route("/api/rungmm", methods=["POST"], strict_slashes=False) 
@cross_origin()
def runGMM():
    request_df = request.get_json()['df']
    num_clusters = request.get_json()['num_clusters']
    if num_clusters < 2:
        num_clusters = 2

    pca_df = pd.json_normalize(request_df)
    try:
        pca_cols = [x for x in pca_df.columns if 'PC' in x or 'TSNE' in x or 'UMAP' in x]
    except:
        pca_cols = pca_df.columns
    
    if not pca_cols:
        pca_cols = pca_df.columns

    gmm = GaussianMixture(n_components=num_clusters, random_state=123)
    gmm.fit(pca_df[pca_cols])
    labels = gmm.predict(pca_df[pca_cols])

    return jsonify({'result': list(map(lambda x: int(x), labels))})


# @app.route("/api/rundbscan", methods=["POST"], strict_slashes=False) #NEW
# @cross_origin()
# def runDBSCAN():
#   request_df = request.get_json()['df']
#   eps = request.get_json()['eps']
#   min_samples = request.get_json()['min_samples']
#   pca_df = pd.json_normalize(request_df)

#   try:
#     pca_cols = [x for x in pca_df.columns if 'PC' in x or 'TSNE' in x]
#   except:
#     pca_cols = pca_df.columns

#   if not pca_cols:
#     pca_cols = pca_df.columns

#   dbscan = DBSCAN(eps=eps, min_samples=min_samples).fit(pca_df[pca_cols])
#   clusters = dbscan.labels_
  
#   return jsonify({'result': list(map(lambda x: int(x), clusters))})

@app.route("/api/runhc", methods=["POST"], strict_slashes=False) #3 runs when running the ClusteringAlgorithmsTab when the algo chosen is hierarchical clustering
@cross_origin()
def runHC():
    request_df = request.get_json()['df']
    num_clusters = request.get_json()['num_clusters']
    if num_clusters < 2:
        num_clusters = 2
    pca_df = pd.json_normalize(request_df, max_level=0)
    try:
        pca_cols = [x for x in pca_df.columns if 'PC' in x or 'TSNE' in x or 'UMAP' in x]
    except:
        pca_cols = pca_df.columns
    
    if not pca_cols:
        pca_cols = pca_df.columns
    hc = AgglomerativeClustering(n_clusters=num_clusters, metric='euclidean', linkage='ward').fit_predict(pca_df[pca_cols])
    
    plt.figure(figsize=(10, 7))
    dendrogram(linkage(pca_df[pca_cols], method='ward'))
    plt.xticks([])
    filename = random_string(12)
    plt.savefig(f'./data/dendrogram/{filename}.png')
    return {
        'result': list(map(lambda x: int(x), hc)), 
        'filename': filename + ".png"
    }

@app.route("/api/dendrogram/<image_name>", methods=["GET"], strict_slashes=False) #4 runs inside centralPane Dendrogram tab
@cross_origin()
def dendrogramImage(image_name):
    return send_file(f'./data/dendrogram/{image_name}')

@app.route("/api/runfuzzy", methods=["POST"], strict_slashes=False) #5 runs when running the ClusteringAlgorithmsTab when the algo chosen is fuzzy c-means
@cross_origin()
def runFuzzy():
    request_df = request.get_json()['df']
    num_clusters = request.get_json()['num_clusters']
    if num_clusters < 2:
        num_clusters = 2
    pca_df = pd.json_normalize(request_df)
    try:
        pca_cols = [x for x in pca_df.columns if 'PC' in x or 'TSNE' in x or 'UMAP' in x]
    except:
        pca_cols = pca_df.columns
    
    if not pca_cols:
        pca_cols = pca_df.columns

    fcm = FCM(n_clusters=num_clusters, random_state=111,  max_iter=1000)
    pca_df = pca_df[pca_cols].astype('float64')
    pca_df1 = pca_df.to_numpy()
    fcm.fit(pca_df1)
    fuzzy = fcm.predict(pca_df1)
    return jsonify(list(map(lambda x: int(x), fuzzy)))

@app.route("/api/cmtsne2d", methods=["POST"], strict_slashes=False) #6
@cross_origin()
def cmtsne2d():
    request_df = request.get_json()['df']
    pca_df = pd.json_normalize(request_df)
    try:
        pca_cols = [x for x in pca_df.columns if 'PC' in x or 'TSNE' in x ]
        other_cols = [x for x in pca_df.columns if 'PC' not in x and 'TSNE' not in x]
        if not pca_cols:
            pca_cols = pca_df.columns
            other_cols = []
    except:
        pca_cols = pca_df.columns
    
    tsne_visualization = TSNE(random_state=123).fit_transform(pca_df[pca_cols])
    tsne_df = pd.DataFrame(tsne_visualization)
    tsne_df.columns = ["TSNE-1", "TSNE-2"]
    results_df = pd.concat([tsne_df, pca_df[other_cols]], axis=1)
    return results_df.to_csv()

@app.route("/api/cmtsne3d", methods=["POST"], strict_slashes=False) #7
@cross_origin()
def cmtsne3d():
    request_df = request.get_json()['df']
    pca_df = pd.json_normalize(request_df)
    try:
        pca_cols = [x for x in pca_df.columns if 'PC' in x or 'TSNE' in x]
        other_cols = [x for x in pca_df.columns if 'PC' not in x and 'TSNE' not in x]
        if not pca_cols:
            pca_cols = pca_df.columns
            other_cols = []
    except:
        pca_cols = pca_df.columns
    
    tsne_visualization = TSNE(n_components=3, random_state=123).fit_transform(pca_df[pca_cols])
    tsne_df = pd.DataFrame(tsne_visualization)
    tsne_df.columns = ["TSNE-1", "TSNE-2", "TSNE-3"]
    results_df = pd.concat([tsne_df, pca_df[other_cols]], axis=1)
    return results_df.to_csv()

@app.route("/api/cmumap2d", methods=["POST"], strict_slashes=False)
@cross_origin()
def cmumap2d():
    request_df = request.get_json()['df']
    pca_df = pd.json_normalize(request_df)
    try:
        pca_cols = [x for x in pca_df.columns if 'PC' in x or 'UMAP' in x]
        other_cols = [x for x in pca_df.columns if 'PC' not in x and 'UMAP' not in x]
        if not pca_cols:
            pca_cols = pca_df.columns
            other_cols = []
    except:
        pca_cols = pca_df.columns

    umap_visualization = UMAP(random_state=123).fit_transform(pca_df[pca_cols])
    umap_df = pd.DataFrame(umap_visualization)
    umap_df.columns = ["UMAP-1", "UMAP-2"]
    results_df = pd.concat([umap_df, pca_df[other_cols]], axis=1)
    return results_df.to_csv()

@app.route("/api/cmumap3d", methods=["POST"], strict_slashes=False)
@cross_origin()
def cmumap3d():
    request_df = request.get_json()['df']
    pca_df = pd.json_normalize(request_df)
    try:
        pca_cols = [x for x in pca_df.columns if 'PC' in x or 'UMAP' in x]
        other_cols = [x for x in pca_df.columns if 'PC' not in x and 'UMAP' not in x]
        if not pca_cols:
            pca_cols = pca_df.columns
            other_cols = []
    except:
        pca_cols = pca_df.columns

    umap_visualization = UMAP(n_components=3, random_state=123).fit_transform(pca_df[pca_cols])
    umap_df = pd.DataFrame(umap_visualization)
    umap_df.columns = ["UMAP-1", "UMAP-2", "UMAP-3"]
    results_df = pd.concat([umap_df, pca_df[other_cols]], axis=1)
    return results_df.to_csv()

@app.route("/api/uploadCM", methods=["POST"], strict_slashes=False) #8
@cross_origin()
def uploadCM():
    target = './data/test_docs'
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files['file']
    filename = random_string(12)
    extension = '.' + file.filename.split('.')[-1]
    destination = "/".join([target, filename])
    file.save(destination + extension)
    
    if extension == ".pkl":
        cm_df = pickle.load(open(destination + extension, "rb"))
    else:
        cm_df = pd.read_csv(destination + extension)

    try:
        components = min(20, len(cm_df.columns))
        pca_new = PCA(n_components=components)
        principalComponents_new = pca_new.fit_transform(cm_df)
    except:
        cm_df = pd.read_csv(destination + extension, sep=" ")
        components = min(20, len(cm_df.columns))
        pca_new = PCA(n_components=components)
        principalComponents_new = pca_new.fit_transform(cm_df)
        
    response_df = pd.DataFrame(principalComponents_new)
    response_df.columns = ['PC' + (str(i + 1)) for i in range(components)]
    print(response_df)
    return response_df.to_csv()

def random_string(length):
    pool = string.ascii_letters + string.digits
    return ''.join(random.choice(pool) for i in range(length))

@app.route('/api/uploadPCAIR', methods=['POST']) #9
@cross_origin()
def uploadPCAIR():
    target = './data/test_docs'
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files['file'] 
    filename = random_string(12)
    extension = '.' + file.filename.split('.')[-1]
    destination = "/".join([target, filename])
    file.save(destination + extension)
    
    return {'filename': filename}

@app.route('/api/runPCAIR', methods=['POST']) #10
@cross_origin()
def runPCAIR():
    bed_name = request.get_json()['bedName']
    bim_name = request.get_json()['bimName']
    fam_name = request.get_json()['famName']
    kinship_name = request.get_json()['kinshipName']
    gds_name = random_string(12)
    result_name = random_string(12)
    if kinship_name == "":
        robjects.r('''
        .libPaths("/home/local/QCRI/kisufaj/R/x86_64-pc-linux-gnu-library/4.1")
        library(GENESIS)
        library(SNPRelate)
        library(GWASTools)
        showfile.gds(closeall=TRUE)
        snpgdsBED2GDS(bed.fn = "./data/test_docs/%s.bed", bim.fn = "./data/test_docs/%s.bim", fam.fn ="./data/test_docs/%s.fam", out.gdsfn = "./data/test_docs/%s.gds")

        geno <- GdsGenotypeReader(filename = "./data/test_docs/%s.gds")
        genoData <- GenotypeData(geno)
        
        IDs <- read.table("./data/test_docs/%s.fam", header = FALSE)
        IDs_col <- IDs[,1]

        pcair_result_nokin <- pcair(gdsobj = genoData, kinobj = NULL, divobj = NULL, num.cores = 32)  ## Normal PCA

        pc_vectors_nokin <- as.data.frame(pcair_result_nokin$vectors[,c(1:20)])
        pc_vectors_nokin$IID <- as.character(IDs$V1)

        colnames(pc_vectors_nokin)[1:20] = paste("PC",1:20,sep="")
        write.csv(pc_vectors_nokin, "./data/test_docs/%s.csv", row.names=F,col.names=TRUE)
        ''' % (bed_name, bim_name, fam_name, gds_name, gds_name, fam_name, result_name))
    else:
        robjects.r('''
        .libPaths("/home/local/QCRI/kisufaj/R/x86_64-pc-linux-gnu-library/4.1")
        library(GENESIS)
        library(SNPRelate)
        library(GWASTools)
        showfile.gds(closeall=TRUE)
        snpgdsBED2GDS(bed.fn = "./data/test_docs/%s.bed", bim.fn = "./data/test_docs/%s.bim", fam.fn ="./data/test_docs/%s.fam", out.gdsfn = "./data/test_docs/%s.gds")

        geno <- GdsGenotypeReader(filename = "./data/test_docs/%s.gds")
        genoData <- GenotypeData(geno)
        
        kinship <- read.table("./data/test_docs/%s.txt", header = FALSE)
        IDs <- read.table("./data/test_docs/%s.fam", header = FALSE)

        IDs_col <- IDs[,1]

        colnames(kinship) <- IDs_col
        rownames(kinship) <- IDs_col
        pcair_result       <- pcair(gdsobj = genoData, kinobj = as.matrix(kinship), divobj = as.matrix(kinship), div.thresh= -2^(-9/2), kin.thresh=2^(-9/2), num.cores = 4) ## PC-air

        pc_vectors <- as.data.frame(pcair_result$vectors[,c(1:20)])
        pc_vectors$IID <- as.character(IDs$V1) 

        colnames(pc_vectors)[1:20] = paste("PC",1:20,sep="")
        write.csv(pc_vectors, "./data/test_docs/%s.csv", row.names=F,col.names=TRUE)
        ''' % (bed_name, bim_name, fam_name, gds_name, gds_name, kinship_name, fam_name, result_name))
    
    return pd.read_csv(f'./data/test_docs/{result_name}.csv').to_csv()

@app.route("/api/detectoutliers", methods=["POST"], strict_slashes=False) #11
@cross_origin()
def detectoutliers():
    def choose_columns(x):
        if input_format == "pca":
            return ('PC%d' % (x))
        elif input_format == "umap":
            return ('UMAP-%d' % (x+1))
        else:    
            return ('TSNE-%d' % (x))

    def binary(x):
        if x == 1:
            return 1
        return 0

    def outliers(x):
        if x == 1:
            return 0
        return 1
        
    request_df = request.get_json()['df']
    request_method = request.get_json()['method']
    column_range_req = request.get_json()['columnRange']
    if column_range_req[0] > column_range_req[1]:
        column_range = list(range(column_range_req[1], column_range_req[0] + 1))
    else:    
        column_range = list(range(column_range_req[0], column_range_req[1] + 1)) # [1,2,3,4,5,6,7,8,9,10]

    combine_type = int(request.get_json()['combineType'])
    std_freedom = int(request_method)
    input_format = request.get_json()['inputFormat']
    df = pd.json_normalize(request_df)
    newdf = {}
    columns_of_interest = list(map(choose_columns, column_range))
    
    #Isolation Forest
    if std_freedom == 4:
        clf = IsolationForest(contamination=0.1, random_state=123).fit_predict(df[columns_of_interest])
        clf_binary = {0: list(map(outliers, clf))}
        clf_df = pd.DataFrame(clf_binary)
        return clf_df.to_csv()
    
    #MCD
    if std_freedom == 5:
        clf = EllipticEnvelope(contamination=0.01).fit_predict(df[columns_of_interest])
        clf_binary = {0: list(map(outliers, clf))}
        clf_df = pd.DataFrame(clf_binary)
        return clf_df.to_csv()
    
    #Local Outlier Factor
    if std_freedom == 6:
        clf = LocalOutlierFactor(n_neighbors=20, contamination=.03).fit_predict(df[columns_of_interest])
        clf_binary = {0: list(map(outliers, clf))}
        clf_df = pd.DataFrame(clf_binary)
        return clf_df.to_csv()
    
    #One-Class SVM
    if std_freedom == 7:
        clf = OneClassSVM(kernel='rbf').fit_predict(df[columns_of_interest])
        clf_binary = {0: list(map(outliers, clf))}
        clf_df = pd.DataFrame(clf_binary)
        return clf_df.to_csv()


    # K-Nearest Neighbors (KNN)
    if std_freedom == 8:
        clf = KNeighborsClassifier(n_neighbors=5).fit(df[columns_of_interest], df[columns_of_interest])
        distances, _ = clf.kneighbors(df[columns_of_interest])
        mean_distances = distances.mean(axis=1)
        threshold = mean_distances.mean() + 2 * mean_distances.std()
        outliers_list = [1 if distance > threshold else 0 for distance in mean_distances]
        clf_binary = {0: list(map(outliers, outliers_list))}
        clf_df = pd.DataFrame(clf_binary)
        return clf_df.to_csv()
    
    #Standard Deviation
    for col in columns_of_interest:
        if col in df.columns:
            pcx = df.loc[:, col]
            pcx = pd.Series(pcx, dtype='float')
            data_mean, data_std = (pcx.mean()), (pcx.std())
            cut_off = data_std * std_freedom
            lower, upper = data_mean - cut_off, data_mean + cut_off

            outliers = [(1 if x < lower or x > upper else 0) for x in pcx]
            newdf[col] = outliers

    outliers_result = pd.DataFrame(newdf)
    
    if combine_type == 0:
        apply_combineType = outliers_result.aggregate(lambda x: all(x), axis=1)
    else:
        apply_combineType = outliers_result.aggregate(lambda x: any(x), axis=1)
    
    change_to_binary = apply_combineType.apply(binary)
    return change_to_binary.to_csv()

@app.route("/api/samplePCA/<sample_id>", methods=["GET"], strict_slashes=False) #this endpoint is not being used
@cross_origin()
def samplePCA(sample_id):
    if int(sample_id) == 0:
        pca_sample_path = './datasets/KG_PCS.csv'
        pca_sample = pd.read_csv(pca_sample_path)
    else:
        pca_sample_path = './datasets/HGDP/hgdp.csv'
        pca_sample = pd.read_csv(pca_sample_path)
    return pca_sample.to_csv()

@app.route("/api/sampleAdmix", methods=["GET"], strict_slashes=False) #12
@cross_origin()
def sampleAdmix():
    admix_sample_path = './datasets/admix_KG.5.Q'
    admix_sample = pd.read_csv(admix_sample_path, sep=' ')
    return admix_sample.to_csv(index=False, sep=' ')

@app.route("/api/samplePCAAdmixDataset/<sample_id>", methods=["GET"], strict_slashes=False) #13
@cross_origin()
def samplePCAAdmixDataset(sample_id):
    if int(sample_id) == 0:
        pca_sample_path = './datasets/KG_PCS.csv'
        admix_sample_path = './datasets/admix_KG.5.Q'
    else:
        pca_sample_path = './datasets/HGDP/hgdp.csv'
        admix_sample_path = './datasets/HGDP/hgdp.Q'
    
    pca_sample = pd.read_csv(pca_sample_path)
    admix_sample = pd.read_csv(admix_sample_path, sep=' ')

    return {
        "pca": pca_sample.to_csv(), 
        "admix": admix_sample.to_csv(index=False, sep=' ')
    }

@app.route("/api/")
@cross_origin()
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"



@app.route('/register', methods=['POST'],  strict_slashes=False)
@cross_origin(supports_credentials=True)
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        conn = sqlite3.connect('popMLViz.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
        conn.commit()
        c.execute("select * from users") #remove this later
        c.fetchall()
        conn.close()
        return jsonify(message="User registered successfully"), 201 
    except sqlite3.IntegrityError:
        return jsonify(message="User already exists"), 409


@app.route('/login', methods=['POST'],  strict_slashes=False)
@cross_origin(supports_credentials=True)
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = sqlite3.connect('popMLViz.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = c.fetchone()
    conn.close()

    if not user:
        return jsonify(message="User not found"), 404

    if user and bcrypt.check_password_hash(user[2], password):
        response = make_response(jsonify(message="User logged in successfully"), 200)
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)

        response.set_cookie('access_token_cookie', access_token, httponly=True, secure=True, samesite='none', max_age=15*60 ) #secure=true means the token get sent only wehn the connection is https 
        response.set_cookie('refresh_token_cookie', refresh_token, httponly=True,secure=True, samesite='none', max_age=30*24*60*60)
        #note that access token duration is 15 minutes and refresh token duration is 30 days
        return response

    else:
        return jsonify(message="Invalid credentials"), 401



@app.route('/verify', methods=['GET'])
@cross_origin(supports_credentials=True)
@jwt_required()
def verify():
    current_user = get_jwt_identity()
    return jsonify(user=current_user), 200

@app.route('/api/deletePlot', methods=['POST'])
@cross_origin(supports_credentials=True)
@jwt_required()
def delete_plot():
    current_user = get_jwt_identity()
    data = request.get_json()

    plot_title = data.get('title')
    conn = sqlite3.connect('popMLViz.db')
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM plots WHERE user_id=? AND plot_title = ?", (current_user, plot_title,))
    conn.commit()
    conn.close()
    return jsonify({"plot": "Plot deleted successfully"}), 200

@app.route('/save', methods=['POST'])
@cross_origin(supports_credentials=True)
@jwt_required()
def save_plot():
    current_user = get_jwt_identity()
    data = request.get_json()

    plot_title = data.get('name')
    data_plot = data.get('data')
    axis_labels = data.get('axis')
    isOr = data.get('isOr')
    clusteringAlgo = data.get('clusteringAlgo')
    numCluster = data.get("numClusters")
    outlierDetectionAlgo = data.get("outlierDetectionAlgo")
    outlierDetectionColumnsStart = data.get("outlierDetectionColumnsStart")
    outlierDetectionColumnsEnd = data.get("outlierDetectionColumnsEnd")
    selectedUploadOption = data.get("selectedUploadOption")


    if not plot_title or not data_plot:
        return jsonify({"error": "Missing required fields"}), 400

    if isOr:
        if isOr == True:
            isOr = 1
        else:
            isOr = 0 

    # Convert data_plot to JSON string
    data_plot_json = json.dumps(data_plot)
    axis_labels = json.dumps(axis_labels)

    conn = sqlite3.connect('popMLViz.db')
    c = conn.cursor()
    c.execute("SELECT id FROM plots WHERE plot_title=? AND user_id=?", (plot_title, current_user))
    existing_plot = c.fetchone()

    if existing_plot:
        conn.close()
        return jsonify({"error": "Plot title already exists for this user"}), 400


    c.execute('''INSERT INTO plots (data_plot, plot_title, axis_labels, user_id, is_or, clustering_algorithm, 
                                    number_of_clusters, outlier_detection, outlier_Detection_column_start, 
                                    outlier_Detection_column_end, selected_upload_option) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (data_plot_json, plot_title, axis_labels, current_user, isOr, clusteringAlgo, numCluster, 
               outlierDetectionAlgo, outlierDetectionColumnsStart, outlierDetectionColumnsEnd, selectedUploadOption))
    conn.commit()           
    conn.close()

    return jsonify({"plot": "Plot saved successfully"}), 201

@app.route('/api/getSavedData', methods=['GET'])
@cross_origin(supports_credentials=True)
@jwt_required()
def get_plots():
    current_user = get_jwt_identity()

    conn = sqlite3.connect('popMLViz.db')
    c = conn.cursor()
    c.execute("SELECT date_created, plot_title, axis_labels, is_or,clustering_algorithm, number_of_clusters, outlier_detection, outlier_Detection_column_start, outlier_Detection_column_end, selected_upload_option  FROM plots WHERE user_id=?", (current_user,))
    plots = c.fetchall()
    conn.close()

    plot_list = []

    for plot in plots:
        # plot_data = json.loads(plot[0])
        plot_list.append({
            "title": plot[1],
            "date": plot[0],
            "axis": plot[2],
            "isOr": plot[3],
            "clusteringAlgo": plot[4],
            "numCluster": plot[5],
            "outlierDetectionAlgo": plot[6],
            "outlierDetectionColumnsStart": plot[7],
            "outlierDetectionColumnsEnd": plot[8],
            "selectedUploadOption": plot[9]
        })
    return jsonify({"plots": plot_list}), 200

@app.route('/api/getSavedPlot', methods=['GET'])
@cross_origin(supports_credentials=True)
@jwt_required()
def get_plot():
    current_user = get_jwt_identity()
    plot_title = request.args.get('name')
    print(plot_title)  # Debugging: print the plot title received

    conn = sqlite3.connect('popMLViz.db')
    c = conn.cursor()
    c.execute("SELECT date_created, data_plot, plot_title, axis_labels, is_or,clustering_algorithm, number_of_clusters, outlier_detection, outlier_Detection_column_start, outlier_Detection_column_end, selected_upload_option FROM plots WHERE user_id=? AND plot_title=?", (current_user, plot_title))
    plot = c.fetchone()  # Fetch one plot
    conn.close()

    # if plot[4]:
    #     if plot[4] == 1:
    #         plot[4] = True
    #     else:
    #         plot[4] = False    

    if plot:
        plot_data = {
            "date": plot[0],
            "plot": json.loads(plot[1]) ,
            "title": plot[2],
            "axis": json.loads(plot[3]) if plot[3] else None,
            "isOr": plot[4],
            "clusteringAlgo": plot[5],
            "numCluster": plot[6],
            "outlierDetectionAlgo": plot[7],
            "outlierDetectionColumnsStart": plot[8],
            "outlierDetectionColumnsEnd": plot[9],
            "selectedUploadOption": plot[10]
        }
        return jsonify({"plot": plot_data}), 200
    else:
        return jsonify({"error": "Plot not found"}), 404


@app.route('/refresh', methods=['POST'])
@cross_origin(supports_credentials=True)
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    response = make_response(jsonify(access_token=new_access_token), 200)
    response.set_cookie('access_token_cookie', new_access_token, httponly=True,secure=True, samesite='none', max_age=15*60 )
    return response


@app.route('/logout', methods=['POST'])
@cross_origin(supports_credentials=True)
@jwt_required(refresh=True)
def logout():
    response = make_response(jsonify({"message": "Successfully logged out"}), 200)
    response.set_cookie('access_token_cookie', "", httponly=True,secure=True, samesite='none', max_age=0)
    response.set_cookie('refresh_token_cookie', "", httponly=True,secure=True, samesite='none', max_age=0)
    return response

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)