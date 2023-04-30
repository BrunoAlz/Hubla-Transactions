import Layout from "../Layout";
import { useDispatch, useSelector } from "react-redux";
import { useEffect } from "react";
import { contractTransactions } from "../../slices/contracts/contractsSlice";
import { useNavigate, useParams } from "react-router-dom";
import TransactionsTable from "../../components/TransactionsTable";
import { toast } from "react-toastify";
import notFound404 from "../notFound404";

const ContractsTransactions = () => {
  const { transactions, contracts, isLoading, isError, isSuccess, message } =
    useSelector((state) => state.contracts);
  const dispatch = useDispatch();
  const { contract_id } = useParams();
  const navigate = useNavigate();
  useEffect(() => {
    if (isError) {
      toast.error(message);
      navigate(notFound404);
    }
    dispatch(contractTransactions(contract_id));
  }, [isError]);

  return (
    <div>
      <Layout />
      <div className="container-fluid">
        <div className="row">
          <main className="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <h1 className="mt-3">
              Contract N° {contract_id} - Register date {contracts}
            </h1>
            {transactions ? <TransactionsTable props={transactions} /> : "A"}
          </main>
        </div>
      </div>
    </div>
  );
};

export default ContractsTransactions;
