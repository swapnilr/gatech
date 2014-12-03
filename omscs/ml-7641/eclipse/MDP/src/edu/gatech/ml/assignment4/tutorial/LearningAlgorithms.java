package edu.gatech.ml.assignment4.tutorial;

import java.awt.Color;
import java.util.Deque;
import java.util.LinkedList;
import java.util.List;
import java.util.Stack;

import burlap.behavior.singleagent.EpisodeAnalysis;
import burlap.behavior.singleagent.EpisodeSequenceVisualizer;
import burlap.behavior.singleagent.Policy;
import burlap.behavior.singleagent.QValue;
import burlap.oomdp.singleagent.Action;
import burlap.oomdp.singleagent.SADomain;
import burlap.behavior.singleagent.auxiliary.StateReachability;
import burlap.behavior.singleagent.auxiliary.performance.LearningAlgorithmExperimenter;
import burlap.behavior.singleagent.auxiliary.performance.PerformanceMetric;
import burlap.behavior.singleagent.auxiliary.performance.TrialMode;
import burlap.behavior.singleagent.auxiliary.valuefunctionvis.ValueFunctionVisualizerGUI;
import burlap.behavior.singleagent.auxiliary.valuefunctionvis.common.ArrowActionGlyph;
import burlap.behavior.singleagent.auxiliary.valuefunctionvis.common.LandmarkColorBlendInterpolation;
import burlap.behavior.singleagent.auxiliary.valuefunctionvis.common.PolicyGlyphPainter2D;
import burlap.behavior.singleagent.auxiliary.valuefunctionvis.common.PolicyGlyphPainter2D.PolicyGlyphRenderStyle;
import burlap.behavior.singleagent.auxiliary.valuefunctionvis.common.StateValuePainter2D;
import burlap.behavior.singleagent.learning.GoalBasedRF;
import burlap.behavior.singleagent.learning.LearningAgent;
import burlap.behavior.singleagent.learning.LearningAgentFactory;
import burlap.behavior.singleagent.learning.tdmethods.QLearning;
import burlap.behavior.singleagent.planning.OOMDPPlanner;
import burlap.behavior.singleagent.planning.QComputablePlanner;
import burlap.behavior.singleagent.planning.StateConditionTest;
import burlap.behavior.singleagent.planning.commonpolicies.GreedyQPolicy;
import burlap.behavior.singleagent.planning.deterministic.DeterministicPlanner;
import burlap.behavior.singleagent.planning.deterministic.SDPlannerPolicy;
import burlap.behavior.singleagent.planning.deterministic.TFGoalCondition;
import burlap.behavior.singleagent.planning.deterministic.informed.Heuristic;
import burlap.behavior.singleagent.planning.deterministic.informed.astar.AStar;
import burlap.behavior.singleagent.planning.deterministic.uninformed.bfs.BFS;
import burlap.behavior.singleagent.planning.deterministic.uninformed.dfs.DFS;
import burlap.behavior.singleagent.planning.stochastic.policyiteration.PolicyIteration;
import burlap.behavior.singleagent.planning.stochastic.valueiteration.ValueIteration;
import burlap.behavior.statehashing.DiscreteStateHashFactory;
import burlap.behavior.statehashing.NameDependentStateHashFactory;
import burlap.behavior.statehashing.StateHashFactory;
import burlap.domain.singleagent.gridworld.GridWorldDomain;
import burlap.domain.singleagent.gridworld.GridWorldStateParser;
import burlap.domain.singleagent.gridworld.GridWorldVisualizer;
import burlap.domain.singleagent.lunarlander.LLStateParser;
import burlap.domain.singleagent.lunarlander.LLVisualizer;
import burlap.domain.singleagent.lunarlander.LunarLanderDomain;
import burlap.domain.singleagent.lunarlander.LunarLanderRF;
import burlap.domain.singleagent.lunarlander.LunarLanderTF;
import burlap.oomdp.auxiliary.StateGenerator;
import burlap.oomdp.auxiliary.StateParser;
import burlap.oomdp.auxiliary.common.ConstantStateGenerator;
import burlap.oomdp.core.AbstractGroundedAction;
import burlap.oomdp.core.Domain;
import burlap.oomdp.core.ObjectInstance;
import burlap.oomdp.core.State;
import burlap.oomdp.core.TerminalFunction;
import burlap.oomdp.singleagent.RewardFunction;
import burlap.oomdp.singleagent.common.SinglePFTF;
import burlap.oomdp.singleagent.common.UniformCostRF;
import burlap.oomdp.singleagent.common.VisualActionObserver;
import burlap.oomdp.visualizer.Visualizer;

public class LearningAlgorithms {

	GridWorldDomain				gwdg;
	Domain						domain;
	StateParser					sp;
	RewardFunction				rf;
	TerminalFunction			tf;
	StateConditionTest			goalCondition;
	State						initialState;
	DiscreteStateHashFactory			hashingFactory;
	
	protected class VILearningAgent implements LearningAgent {

		LinkedList<EpisodeAnalysis> eas = new LinkedList<EpisodeAnalysis>();
		int size = 1;
		int iterations = 1;
		
		@Override
		public EpisodeAnalysis runLearningEpisodeFrom(State initialState) {
			//System.out.println("RLE called");
			// TODO Auto-generated method stub
			OOMDPPlanner planner = new ValueIteration(domain, rf, tf, 0.99, hashingFactory, 0.001, iterations);
			planner.planFromState(initialState);
			
			//create a Q-greedy policy from the planner
			Policy p = new GreedyQPolicy((QComputablePlanner)planner);
			EpisodeAnalysis ea = p.evaluateBehavior(initialState, rf, tf);
			eas.addLast(ea);
			if(eas.size() > this.size) {
				eas.removeFirst();
			}
			iterations++;
			return ea;
		}

		@Override
		public EpisodeAnalysis runLearningEpisodeFrom(State initialState,
				int maxSteps) {
			//System.out.println("RLE called with " + maxSteps);
			OOMDPPlanner planner = new ValueIteration(domain, rf, tf, 0.99, hashingFactory, 0.001, 1000);
			planner.planFromState(initialState);
			
			//create a Q-greedy policy from the planner
			Policy p = new GreedyQPolicy((QComputablePlanner)planner);
			EpisodeAnalysis ea = p.evaluateBehavior(initialState, rf, tf, maxSteps);
			eas.addLast(ea);
			if(eas.size() > this.size) {
				eas.removeFirst();
			}
			return ea;
		}

		@Override
		public EpisodeAnalysis getLastLearningEpisode() {
			// TODO Auto-generated method stub
			System.out.println("GLLE called");
			return eas.getLast();
		}

		@Override
		public void setNumEpisodesToStore(int numEps) {
			// TODO Auto-generated method stub
			System.out.println("SNETS called with " + numEps);
			this.size = numEps;
			
		}

		@Override
		public List<EpisodeAnalysis> getAllStoredLearningEpisodes() {
			// TODO Auto-generated method stub
			System.out.println("GASLE called when size is " + eas.size());
			return eas;
		}
		
	}

	protected class PILearningAgent implements LearningAgent {

		LinkedList<EpisodeAnalysis> eas = new LinkedList<EpisodeAnalysis>();
		int size = 1;
		int iterations = 1;
		double gamma = 0.99;
		
		@Override
		public EpisodeAnalysis runLearningEpisodeFrom(State initialState) {
			// TODO Auto-generated method stub
			OOMDPPlanner planner = new PolicyIteration(domain, rf, tf, gamma, hashingFactory, 0.001, 0.001, iterations, iterations);
			planner.planFromState(initialState);
			
			//create a Q-greedy policy from the planner
			Policy p = new GreedyQPolicy((QComputablePlanner)planner);
			EpisodeAnalysis ea = p.evaluateBehavior(initialState, rf, tf);
			eas.addLast(ea);
			if(eas.size() > this.size) {
				eas.removeFirst();
			}
			iterations++;
			return ea;
		}

		@Override
		public EpisodeAnalysis runLearningEpisodeFrom(State initialState,
				int maxSteps) {
			OOMDPPlanner planner = new PolicyIteration(domain, rf, tf, 0.99, hashingFactory, 0.001, 0.001, 100, 100);
			planner.planFromState(initialState);
			
			//create a Q-greedy policy from the planner
			Policy p = new GreedyQPolicy((QComputablePlanner)planner);
			EpisodeAnalysis ea = p.evaluateBehavior(initialState, rf, tf, maxSteps);
			eas.addLast(ea);
			if(eas.size() > this.size) {
				eas.removeFirst();
			}
			return ea;
		}

		@Override
		public EpisodeAnalysis getLastLearningEpisode() {
			// TODO Auto-generated method stub
			return eas.getLast();
		}

		@Override
		public void setNumEpisodesToStore(int numEps) {
			// TODO Auto-generated method stub
			this.size = numEps;
			
		}

		@Override
		public List<EpisodeAnalysis> getAllStoredLearningEpisodes() {
			// TODO Auto-generated method stub
			return eas;
		}
		
	}

	
	private int setSmallDomain() {
		int size = 3;
		gwdg = new GridWorldDomain(size, size);
		gwdg.setCellWallState(0, 2, 1);
		gwdg.setCellWallState(1, 0, 1);
		gwdg.setCellWallState(0, 0, 0);
		gwdg.setCellWallState(size - 1, size - 1, 0);
		this.domain = gwdg.generateDomain();
		return size;
	}
	
	private int setLargeDomain() {
		int size = 24;
		gwdg = new GridWorldDomain(size, size);
		for (int i=0; i<size; i+=8) {
			for(int j=0; j<size-1; j++) {
				if(i+2 < size) {
					gwdg.setCellWallState(i + 2, j, 1);	
				}
			}
			for(int j=size-1; j>0; j--) {
				if (i+6 < size) {
					gwdg.setCellWallState(i + 6, j, 1);	
				}
				
			}
		}
		gwdg.setCellWallState(size - 1, size - 1, 0);
		this.domain = gwdg.generateDomain();
		return size;
	}
	
	public LearningAlgorithms(){
		//create the domain
		//int size = setSmallDomain();
		int size = setLargeDomain();
		
		
		//create the state parser
		sp = new GridWorldStateParser(domain); 
		
		//define the task
		rf = new UniformCostRF(); 
		
		tf = new SinglePFTF(domain.getPropFunction(GridWorldDomain.PFATLOCATION)); 
		goalCondition = new TFGoalCondition(tf);
		//rf = new GoalBasedRF(this.goalCondition, 50., -0.1);
		
		//set up the initial state of the task
		initialState = GridWorldDomain.getOneAgentOneLocationState(domain);
		GridWorldDomain.setAgent(initialState, 0, 0);
		GridWorldDomain.setLocation(initialState, 0, size-1, size - 1);
		
		//set up the state hashing system
		hashingFactory = new DiscreteStateHashFactory();
		hashingFactory.setAttributesForClass(GridWorldDomain.CLASSAGENT, 
		domain.getObjectClass(GridWorldDomain.CLASSAGENT).attributeList); 
		
		/*VisualActionObserver observer = new VisualActionObserver(domain, 
				GridWorldVisualizer.getVisualizer(gwdg.getMap()));
		((SADomain)this.domain).setActionObserverForAllAction(observer);
		observer.initGUI();*/
		

		/*LunarLanderDomain lld = new LunarLanderDomain();
		domain = lld.generateDomain();
		sp = new LLStateParser(domain);
		rf = new LunarLanderRF(domain);
		tf = new LunarLanderTF(domain);
		
		initialState = LunarLanderDomain.getCleanState(domain, 0);
		LunarLanderDomain.setAgent(initialState, 0., 5.0, 0.0);
		LunarLanderDomain.setPad(initialState, 75., 95., 0., 10.);
		hashingFactory = new NameDependentStateHashFactory();
		//hashingFactory = new DiscreteStateHashFactory();
		
		VisualActionObserver observer = new VisualActionObserver(domain,
				LLVisualizer.getVisualizer(lld));
		((SADomain)this.domain).setActionObserverForAllAction(observer);
		observer.initGUI();*/
		
	}
	
	public void visualize(String outputPath){
		Visualizer v = GridWorldVisualizer.getVisualizer(gwdg.getMap());
		EpisodeSequenceVisualizer evis = new EpisodeSequenceVisualizer(v, domain, sp, outputPath);
	}
	
	public void valueFunctionVisualize(QComputablePlanner planner, Policy p){
		List <State> allStates = StateReachability.getReachableStates(initialState, 
			(SADomain)domain, hashingFactory);
		LandmarkColorBlendInterpolation rb = new LandmarkColorBlendInterpolation();
		rb.addNextLandMark(0., Color.RED);
		rb.addNextLandMark(1., Color.BLUE);
		
		StateValuePainter2D svp = new StateValuePainter2D(rb);
		svp.setXYAttByObjectClass(GridWorldDomain.CLASSAGENT, GridWorldDomain.ATTX, 
			GridWorldDomain.CLASSAGENT, GridWorldDomain.ATTY);
		
		PolicyGlyphPainter2D spp = new PolicyGlyphPainter2D();
		spp.setXYAttByObjectClass(GridWorldDomain.CLASSAGENT, GridWorldDomain.ATTX, 
			GridWorldDomain.CLASSAGENT, GridWorldDomain.ATTY);
		spp.setActionNameGlyphPainter(GridWorldDomain.ACTIONNORTH, new ArrowActionGlyph(0));
		spp.setActionNameGlyphPainter(GridWorldDomain.ACTIONSOUTH, new ArrowActionGlyph(1));
		spp.setActionNameGlyphPainter(GridWorldDomain.ACTIONEAST, new ArrowActionGlyph(2));
		spp.setActionNameGlyphPainter(GridWorldDomain.ACTIONWEST, new ArrowActionGlyph(3));
		spp.setRenderStyle(PolicyGlyphRenderStyle.DISTSCALED);
		
		ValueFunctionVisualizerGUI gui = new ValueFunctionVisualizerGUI(allStates, svp, planner);
		gui.setSpp(spp);
		gui.setPolicy(p);
		gui.setBgColor(Color.GRAY);
		gui.initGUI();
}
	public void qvalueFunctionVisualize(QComputablePlanner planner, Policy p){
		List <State> allStates = StateReachability.getReachableStates(initialState, 
			(SADomain)domain, hashingFactory);
		LandmarkColorBlendInterpolation rb = new LandmarkColorBlendInterpolation();
		rb.addNextLandMark(0., Color.RED);
		rb.addNextLandMark(1., Color.BLUE);
		
		StateValuePainter2D svp = new StateValuePainter2D(rb);
		svp.setXYAttByObjectClass(GridWorldDomain.CLASSAGENT, GridWorldDomain.ATTX, 
			GridWorldDomain.CLASSAGENT, GridWorldDomain.ATTY);
		
		PolicyGlyphPainter2D spp = new PolicyGlyphPainter2D();
		spp.setXYAttByObjectClass(GridWorldDomain.CLASSAGENT, GridWorldDomain.ATTX, 
			GridWorldDomain.CLASSAGENT, GridWorldDomain.ATTY);
		spp.setActionNameGlyphPainter(GridWorldDomain.ACTIONNORTH, new ArrowActionGlyph(0));
		spp.setActionNameGlyphPainter(GridWorldDomain.ACTIONSOUTH, new ArrowActionGlyph(1));
		spp.setActionNameGlyphPainter(GridWorldDomain.ACTIONEAST, new ArrowActionGlyph(2));
		spp.setActionNameGlyphPainter(GridWorldDomain.ACTIONWEST, new ArrowActionGlyph(3));
		spp.setRenderStyle(PolicyGlyphRenderStyle.DISTSCALED);
		
		ValueFunctionVisualizerGUI gui = new ValueFunctionVisualizerGUI(allStates, svp, planner);
		gui.setSpp(spp);
		gui.setPolicy(p);
		gui.setBgColor(Color.GRAY);
		gui.initGUI();
}
	
	public void BFSExample(String outputPath){
		
		if(!outputPath.endsWith("/")){
			outputPath = outputPath + "/";
		}
		
		//BFS ignores reward; it just searches for a goal condition satisfying state
		DeterministicPlanner planner = new BFS(domain, goalCondition, hashingFactory); 
		planner.planFromState(initialState);
		
		//capture the computed plan in a partial policy
		Policy p = new SDPlannerPolicy(planner);
		
		//record the plan results to a file
		p.evaluateBehavior(initialState, rf, tf).writeToFile(outputPath + "BFSplanResult", sp);
			
	}
	
	public void DFSExample(String outputPath){
		
		if(!outputPath.endsWith("/")){
			outputPath = outputPath + "/";
		}
		
		//DFS ignores reward; it just searches for a goal condition satisfying state
		DeterministicPlanner planner = new DFS(domain, goalCondition, hashingFactory);
		planner.planFromState(initialState);
		
		//capture the computed plan in a partial policy
		Policy p = new SDPlannerPolicy(planner);
		
		//record the plan results to a file
		p.evaluateBehavior(initialState, rf, tf).writeToFile(outputPath + "DFSplanResult", sp);
		
	}
	
	public void AStarExample(String outputPath){
		
		if(!outputPath.endsWith("/")){
			outputPath = outputPath + "/";
		}
		
		
		Heuristic mdistHeuristic = new Heuristic() {
			
			@Override
			public double h(State s) {
				
				String an = GridWorldDomain.CLASSAGENT;
				String ln = GridWorldDomain.CLASSLOCATION;
				
				ObjectInstance agent = s.getObjectsOfTrueClass(an).get(0); 
				ObjectInstance location = s.getObjectsOfTrueClass(ln).get(0); 
				
				//get agent position
				int ax = agent.getDiscValForAttribute(GridWorldDomain.ATTX);
				int ay = agent.getDiscValForAttribute(GridWorldDomain.ATTY);
				
				//get location position
				int lx = location.getDiscValForAttribute(GridWorldDomain.ATTX);
				int ly = location.getDiscValForAttribute(GridWorldDomain.ATTY);
				
				//compute Manhattan distance
				double mdist = Math.abs(ax-lx) + Math.abs(ay-ly);
				
				return -mdist;
			}
		};
		
		//provide A* the heuristic as well as the reward function so that it can keep
		//track of the actual cost
		DeterministicPlanner planner = new AStar(domain, rf, goalCondition, 
			hashingFactory, mdistHeuristic);
		planner.planFromState(initialState);
		
		
		//capture the computed plan in a partial policy
		Policy p = new SDPlannerPolicy(planner);
		
		//record the plan results to a file
		p.evaluateBehavior(initialState, rf, tf).writeToFile(outputPath + "AStarplanResult", sp);
		
	}	
	
	public void ValueIterationExample(String outputPath, int numIterations){
		
		
		if(!outputPath.endsWith("/")){
			outputPath = outputPath + "/";
		}
		
		
		OOMDPPlanner planner = new ValueIteration(domain, rf, tf, 0.99, hashingFactory, 0.001, numIterations);
		planner.planFromState(initialState);
		
		//create a Q-greedy policy from the planner
		Policy p = new GreedyQPolicy((QComputablePlanner)planner);
		EpisodeAnalysis ea = p.evaluateBehavior(initialState, rf, tf);
		System.out.println(ea.actionSequence.size());
		
		//record the plan results to a file
		ea.writeToFile(outputPath + "VIplanResult", sp);
		
		this.valueFunctionVisualize((QComputablePlanner)planner, p);
		
	}
	
	public void PolicyIterationExample(String outputPath){
		
		if(!outputPath.endsWith("/")){
			outputPath = outputPath + "/";
		}
		
		
		OOMDPPlanner planner = new PolicyIteration(domain, rf, tf, 0.99, hashingFactory, 0.001, 0.001, 100, 100);
		planner.planFromState(initialState);
		
		//create a Q-greedy policy from the planner
		Policy p = new GreedyQPolicy((QComputablePlanner)planner);
		EpisodeAnalysis ea = p.evaluateBehavior(initialState, rf, tf);
		System.out.println(ea.actionSequence.size());
		
		//record the plan results to a file
		p.evaluateBehavior(initialState, rf, tf).writeToFile(outputPath + "PIplanResult", sp);
		
		this.valueFunctionVisualize((QComputablePlanner)planner, p);
		
	}
	
	public void QLearningExample(String outputPath){
		
		if(!outputPath.endsWith("/")){
			outputPath = outputPath + "/";
		}
		
		rf = new GoalBasedRF(this.goalCondition, 5., -1);
		//creating the learning algorithm object; discount= 0.9; initialQ=0.0; learning rate=0.9
		QLearning agent = new QLearning(domain, rf, tf, 0.9, hashingFactory, 0., 0.9);
		
		//run learning for 100 episodes
		for(int i = 0; i < 1000; i++){
			EpisodeAnalysis ea = agent.runLearningEpisodeFrom(initialState);
			ea.writeToFile(String.format("%se%03d", outputPath, i), sp); 
			State currentState = initialState;
		    int size = 0;
			while((!agent.getTF().isTerminal(currentState)) && size < ea.numTimeSteps()) {
				State futureState = null;
				double val = Double.NEGATIVE_INFINITY;
				AbstractGroundedAction a = null;
				for (QValue q: agent.getQs(currentState)) {
					if(q.q > val) {
						val = q.q;
						futureState = q.a.executeIn(currentState);
						a = q.a;
					}
				}
				currentState = futureState;
				//System.out.println(a.actionName());
				size++;
			}
			System.out.println(i + ": " + ea.numTimeSteps() + ", " + size);
		}
		
		
	}
	
	public void experimenterAndPlotter(){
		
		//custom reward function for more interesting results
		//final RewardFunction rf = new GoalBasedRF(this.goalCondition, 5., -0.1);
		final RewardFunction rf = new GoalBasedRF(this.goalCondition, 5., -1);

		/**
		 * Create factories for Q-learning agent and SARSA agent to compare
		 */

		LearningAgentFactory qLearningFactory = new LearningAgentFactory() {
						
			@Override
			public String getAgentName() {
				return "Q-learning: 0.99";
			}
			
			@Override
			public LearningAgent generateAgent() {
				return new QLearning(domain, rf, tf, 0.99, hashingFactory, 0.3, 0.99);
			}
		};

		LearningAgentFactory q1LearningFactory = new LearningAgentFactory() {
			
			@Override
			public String getAgentName() {
				return "Q-learning: 0.9";
			}
			
			@Override
			public LearningAgent generateAgent() {
				return new QLearning(domain, rf, tf, 0.99, hashingFactory, 0.3, 0.9);
			}
		};

		
		LearningAgentFactory q2LearningFactory = new LearningAgentFactory() {
			
			@Override
			public String getAgentName() {
				return "Q-learning: 0.75";
			}
			
			@Override
			public LearningAgent generateAgent() {
				return new QLearning(domain, rf, tf, 0.99, hashingFactory, 0.3, 0.75);
			}
		};

		LearningAgentFactory q3LearningFactory = new LearningAgentFactory() {
			
			@Override
			public String getAgentName() {
				return "Q-learning: 0.50";
			}
			
			@Override
			public LearningAgent generateAgent() {
				return new QLearning(domain, rf, tf, 0.99, hashingFactory, 0.3, 0.5);
			}
		};

		LearningAgentFactory q4LearningFactory = new LearningAgentFactory() {
			
			@Override
			public String getAgentName() {
				return "Q-learning: 0.25";
			}
			
			@Override
			public LearningAgent generateAgent() {
				return new QLearning(domain, rf, tf, 0.99, hashingFactory, 0.3, 0.25);
			}
		};

		
		LearningAgentFactory q5LearningFactory = new LearningAgentFactory() {
			
			@Override
			public String getAgentName() {
				return "Q-learning: 0.10";
			}
			
			@Override
			public LearningAgent generateAgent() {
				return new QLearning(domain, rf, tf, 0.99, hashingFactory, 0.3, 0.1);
			}
		};
		
		LearningAgentFactory VILearningFactory = new LearningAgentFactory() {
			
			@Override
			public String getAgentName() {
				return "Value Iteration";
			}
			
			@Override
			public LearningAgent generateAgent() {
				return new VILearningAgent();
			}
		};

		LearningAgentFactory PILearningFactory = new LearningAgentFactory() {
			
			@Override
			public String getAgentName() {
				return "Policy Iteration - 0.99";
			}
			
			@Override
			public LearningAgent generateAgent() {
				return new PILearningAgent();
			}
		};
		
		LearningAgentFactory PILearningFactory1 = new LearningAgentFactory() {
			
			@Override
			public String getAgentName() {
				return "Policy Iteration - 0.95";
			}
			
			@Override
			public LearningAgent generateAgent() {
				PILearningAgent p = new PILearningAgent();
				p.gamma = 0.95;
				return p;
			}
		};
		
		LearningAgentFactory PILearningFactory2 = new LearningAgentFactory() {
			
			@Override
			public String getAgentName() {
				return "Policy Iteration - 0.90";
			}
			
			@Override
			public LearningAgent generateAgent() {
				PILearningAgent p = new PILearningAgent();
				p.gamma = 0.90;
				return p;
			}
		};
		
		
		LearningAgentFactory PILearningFactory3 = new LearningAgentFactory() {
			
			@Override
			public String getAgentName() {
				return "Policy Iteration - 0.80";
			}
			
			@Override
			public LearningAgent generateAgent() {
				PILearningAgent p = new PILearningAgent();
				p.gamma = 0.80;
				return p;
			}
		};
		
		
		LearningAgentFactory PILearningFactory4 = new LearningAgentFactory() {
			
			@Override
			public String getAgentName() {
				return "Policy Iteration - 0.50";
			}
			
			@Override
			public LearningAgent generateAgent() {
				PILearningAgent p = new PILearningAgent();
				p.gamma = 0.50;
				return p;
			}
		};
		

		
		/*LearningAgentFactory sarsaLearningFactory = new LearningAgentFactory() {
			
			@Override
			public String getAgentName() {
				return "SARSA";
			}
			
			@Override
			public LearningAgent generateAgent() {
				return new SarsaLam(domain, rf, tf, 0.99, hashingFactory, 0.0, 0.1, 1.);
			}
		};*/

		StateGenerator sg = new ConstantStateGenerator(this.initialState);

		LearningAlgorithmExperimenter exp = new LearningAlgorithmExperimenter((SADomain)this.domain, 
			rf, sg, 20, 50, qLearningFactory, q1LearningFactory,q2LearningFactory,q3LearningFactory,q4LearningFactory,q5LearningFactory);//, VILearningFactory, PILearningFactory);

		//exp = new LearningAlgorithmExperimenter((SADomain)this.domain, 
		//		rf, sg, 2, 100, PILearningFactory, PILearningFactory1, PILearningFactory2,PILearningFactory3,PILearningFactory4);//qLearningFactory, VILearningFactory, PILearningFactory);

		
		exp.setUpPlottingConfiguration(500, 250, 2, 1000, 
			TrialMode.MOSTRECENTANDAVERAGE, 
			PerformanceMetric.STEPSPEREPISODE, 
			PerformanceMetric.AVERAGEEPISODEREWARD);

		exp.startExperiment();

		exp.writeStepAndEpisodeDataToCSV("expData");


	}

	
	public static void main(String[] args) {
		LearningAlgorithms example = new LearningAlgorithms();
		String outputPath = "output/"; //directory to record results
		
		//we will call planning and learning algorithms here
		//run example
		//example.BFSExample(outputPath);
		//example.DFSExample(outputPath);
		//example.AStarExample(outputPath);
		//long time = System.nanoTime();
		example.ValueIterationExample(outputPath, 250);
		//long VItime = System.nanoTime();
		//System.out.println("VI TIME = " + (VItime - time)/(1000.0 * 1000 * 1000));
		example.PolicyIterationExample(outputPath);
		//long PItime = System.nanoTime();
		//System.out.println("PI TIME = " + (PItime - VItime)/(1000.0 * 1000 * 1000));*/
		//long time = System.nanoTime();
		example.QLearningExample(outputPath);
		//long PItime = System.nanoTime();
		//System.out.println("PI TIME = " + (PItime - time)/(1000.0 * 1000 * 1000));
		//example.experimenterAndPlotter();
		//run the visualizer
		example.visualize(outputPath);

	
	}

}
