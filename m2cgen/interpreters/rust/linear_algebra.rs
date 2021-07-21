fn add_vectors(v1: Vec<f64>, v2: Vec<f64>) -> Vec<f64> {
    v1.iter().zip(v2.iter()).map(|(&x, &y)| x + y).collect::<Vec<f64>>()
}
fn mul_vector_number(v1: Vec<f64>, num: f64) -> Vec<f64> {
    v1.iter().map(|&i| i * num).collect::<Vec<f64>>()
}
