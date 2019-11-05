from uuid import uuid4

from flask import Flask, request, jsonify
from flask.logging import default_handler
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

states = dict()


# const router = jsonServer.router(path.join(__dirname, "db.json"));

@app.route("/", methods=['GET'])
@cross_origin('*')
def root():
    return jsonify("Ok"), 200


# hex_sign = values.get('sign')


@app.route("/course", methods=['POST'])
def verify_state_change():
    # try:
    values = request.get_json()
    print(values)
    error = validate_course(request.body())
    values = request.get_json()
    if error != "":
        return jsonify(error), 400
    else:
        states = dict(0)
        return jsonify("Ok"), 200
    # hex_sign = values.get('sign')


# server.post("/courses/", function(req, res, next) {
#   const error = validateCourse(req.body);
#   if (error) {
#     res.status(400).send(error);
#   } else {
#     req.body.slug = createSlug(req.body.title); // Generate a slug for new courses.
#     next();
#   }
# });
#
# // Use default router
# server.use(router);
#
# // Start server
# const port = 3001;
# server.listen(port, () => {
#   console.log(`JSON Server is running on port ${port}`);
# });
#
# // Centralized logic
#
# // Returns a URL friendly slug
# function createSlug(value) {
#   return value
#     .replace(/[^a-z0-9_]+/gi, "-")
#     .replace(/^-|-$/g, "")
#     .toLowerCase();


def validate_course(course):
    if not course.title:
        return "Title is required."
    if not course.authorId:
        return "Author is required."
    if not course.category:
        return "Category is required.";
    return ""


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5002, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    # user.sign_new_state(1, 18000, 2000)
    app.logger.removeHandler(default_handler)
    app.run(host='0.0.0.0', port=port)
