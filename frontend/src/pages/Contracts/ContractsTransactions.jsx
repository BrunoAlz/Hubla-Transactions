import Layout from "../Layout";
import { useDispatch, useSelector } from "react-redux";
import { useEffect } from "react";
import { contractTransactions } from "../../slices/contracts/contractsSlice";
import { Link, useNavigate, useParams } from "react-router-dom";
import { toast } from "react-toastify";
import notFound404 from "../notFound404";

const ContractsTransactions = () => {
  const {
    transactions,
    reports,
    contracts,
    isLoading,
    isError,
    isSuccess,
    message,
  } = useSelector((state) => state.contracts);

  const dispatch = useDispatch();

  const { contract_id } = useParams();

  const producer = reports.slice(2, 3);
  console.log(producer);

  useEffect(() => {
    if (isError) {
      toast.error(message);
    }

    dispatch(contractTransactions(contract_id));
  }, []);

  return (
    <div>
      <Layout />
      <div className="container-fluid">
        <div className="row">
          <main className="col-md-9 ms-sm-auto col-lg-10">
            {transactions.length > 0 ? (
              <div className="">
                <h1 className="mt-3 text-center">
                  Transactions - Contract N° {contract_id}
                </h1>
                <Link className="btn btn-primary" to={"/contracts/"}>
                  BACK
                </Link>
                <div className="row">
                  <div className="col-lg-12 col-md-12 col-sm-12">
                    <table className="table table-striped table-sm table-hover text-center mt-3">
                      <thead className="table-dark">
                        <tr className="fw-bold fs-5">
                          <th>N°</th>
                          <th>Nature</th>
                          <th>Description</th>
                          <th>Date</th>
                          <th>Product</th>
                          <th>Price</th>
                          <th>Seller</th>
                          <th>Type</th>
                        </tr>
                      </thead>
                      <tbody>
                        {transactions.map((transaction) => (
                          <tr key={transaction.id}>
                            <th scope="row">{transaction.id}</th>
                            <td>{transaction.nature}</td>
                            <td>{transaction.description}</td>
                            <td>{transaction.date}</td>
                            <td>{transaction.product}</td>
                            <td>{transaction.price}</td>
                            <td>{transaction.seller}</td>
                            <td>{transaction.signal}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                  <div className="col-lg-12 col-md-12  col-sm-12 mt-3">
                    <h3 className="text-center">Final Balance Producer</h3>
                    <table className="table table-striped table-fluid table-sm table-hover text-center mt-3">
                      <thead className="table-dark">
                        <tr className="fw-bold fs-5">
                          <th>Producer</th>
                          <th>Product</th>
                          <th>Sold by Producer</th>
                          <th>Sold by Affiliate</th>
                          <th>Commision Payed</th>
                          <th>Gross Total</th>
                          <th>Final Balance</th>
                        </tr>
                      </thead>
                      <tbody>
                        {reports.map((report, index) => (
                          <tr key={index}>
                            <td>{report.person}</td>
                            <td>{report.product}</td>
                            <td>{report.total_sold_by_producer}</td>
                            <td>{report.total_sold_by_affiliate}</td>
                            <td>{report.total_commission_paid}</td>
                            <td>{report.gross_total}</td>
                            <td>{report.liquid}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            ) : (
              <div className="mt-3 text-center">
                <h3 className="display-1 text-danger">
                  No transactions found.
                </h3>
                <Link className="btn btn-primary" to={"/contracts/"}>
                  BACK
                </Link>
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
};
export default ContractsTransactions;
